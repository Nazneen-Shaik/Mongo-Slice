from django.shortcuts import render_to_response
from django.http import HttpResponse
from pymongo import Connection
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    if request.method == "POST":
        from mpcomp.views import mongoauth
        db = mongoauth(request.POST.get('host'), request.POST.get('port'), request.POST.get('db'), request.POST.get('uid'), request.POST.get('pwd'))

        if not db:
            data = {'login':False}
            return HttpResponse(json.dumps(data))

        else:        
            request.session['host']=request.POST.get('host')
            request.session['port']=request.POST.get('port')
            request.session['db']=request.POST.get('db')
            request.session['uid']=request.POST.get('uid')
            request.session['pwd']=request.POST.get('pwd')
            request.session['login']=True
            data = {'login':True}
            return HttpResponse(json.dumps(data))

    elif 'login' in request.session:
    
        ctx = {}
        connection = Connection(request.session['host'], int(request.session['port'])) #Connect to mongodb
        db = connection[request.session['db']]   
        ctx['collections'] = db.collection_names()
        ctx['db'] = request.session['db']
        return render_to_response('index.html',ctx)

    else:
        c={}
        c.update(csrf(request))
        return render_to_response('login.html',{'csrf_token':c['csrf_token']})


def mlogout(request):
    from django.http import HttpResponseRedirect
    request.session.flush()
    return HttpResponseRedirect('/')


def info(request,coll_name):
    ctxc = {}
    connection = Connection(request.session['host'], int(request.session['port']))
    db = connection[request.session['db']]
    ctxc['count']=db[coll_name].count()
    ctxc['documents'] = list(db[coll_name].find())
    ctxc['collstats'] = db.command("collstats", coll_name)
    ctxc['collections'] = db.collection_names()
    ctxc['db'] = request.session['db']
    ctxc['name'] = coll_name
 
    #db[coll_name].insert({'Name':'Charan','College':'SNIST'})
    return render_to_response('index.html',ctxc)


@csrf_exempt
def insert_doc(request):
    if request.method == 'GET':
        c={}
        c.update(csrf(request))
        return render_to_response('index.html',{'csrf_token':c['csrf_token']})
    print request.POST.get('collection')
    ctxc = {}
    coll_name = request.POST.get('collection')  
    connection = Connection(request.session['host'], int(request.session['port']))
    db = connection[request.session['db']]
    ctxc['count']=db[coll_name].count()
    ctxc['documents'] = list(db[coll_name].find())
    ctxc['collstats'] = db.command("collstats", coll_name)
    ctxc['collections'] = db.collection_names()
    ctxc['db'] = request.session['db']   
    ctxc['name'] = coll_name
    query=request.POST.get('ta')
    print query
    #db[coll_name].insert({'Name':'Rakesh','College':'SNIST'})
    list1=query.split('.')
    db[coll_name].list1[3]
    return render_to_response('index.html',ctxc)
