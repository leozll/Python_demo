#coding=utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time

from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
#from login.models import User
import json
from django.template import RequestContext



from login.models import User
from models import UserForm,QueryForm
import scripts.Query as Query
import scripts.CityDiff as CityDiff
import scripts.AgeDiff as AgeDiff
import scripts.TimeDiff as TimeDiff
import scripts.ShareId as ShareId

#登录
def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #获取的表单数据与数据库进行比较
            user = User.objects.filter(username__exact = username,password__exact = password)
            if user:
                response = HttpResponseRedirect('/success/')
                #将username写入浏览器cookie,失效时间为3600s
                response.set_cookie('username',username,3600)
                return response
            else:
                return HttpResponseRedirect('/login/')
    else:
        uf = UserForm()
    #return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(request))
    return render(request,'login.html',{'uf':uf})


        
def success(request):
    #获取的表单数据与数据库进行比较
    username=request.COOKIES.get('username','')
    userLogin = User.objects.filter(username__exact = username)
    if userLogin:
        if request.method == 'POST':
            uf = QueryForm(request.POST)
            ufDict={'uf':uf}
            queryResult={}
            if uf.is_valid():
                queryDict = {}
                queryDict['consultant'] = uf.cleaned_data['consultant']
                queryDict['order'] = uf.cleaned_data['order']
                queryDict['city'] = uf.cleaned_data['city']
                queryDict['depth'] = uf.cleaned_data['depth']
                queryDict['span'] = uf.cleaned_data['span']
                queryDict['shareId'] = uf.cleaned_data['shareid']

                if request.POST.has_key('query'):
                    queryResult = Query.orderQuery(queryDict)

                if request.POST.has_key('cityDiff'):
                    queryResult=CityDiff.cityDiff(queryDict)
                    List=json.dumps(queryResult['city'],ensure_ascii=False)
                    Count=queryResult['cityCount']
                    queryResult={'List':List,'Count':Count,'Type':'"column"','Title':'"省份转发趋势"','xTitle':'"省份"'}

                if request.POST.has_key('ageDiff'):
                    queryResult=AgeDiff.ageDiff(queryDict)
                    List=json.dumps(queryResult['age'],ensure_ascii=False)
                    Count=queryResult['ageCount']
                    queryResult={'List':List,'Count':Count,'Type':'"line"','Title':'"年龄转发趋势"','xTitle':'"年龄"'}

                if request.POST.has_key('timeDiff'):
                    queryResult=TimeDiff.timeDiff(queryDict)
                    List=json.dumps(queryResult['time'],ensure_ascii=False)
                    Count=queryResult['timeCount']
                    queryResult={'List':List,'Count':Count,'Type':'"line"','Title':'"日期转发趋势"','xTitle':'"日期"'}

                if request.POST.has_key('shareId'):
                    if len(queryDict['shareId'])>0:
                        queryResult = ShareId.shareId(queryDict)
                    queryResult['canvasHeight']='500'
        else:
            uf = QueryForm()
            ufDict={'uf':uf}
            queryResult={}
        dictMerged=dict(ufDict.items()+queryResult.items())
        return render(request,'success.html',dictMerged)
    else:
        response = HttpResponseRedirect('/login')
        return response

def logout(request):
    #获取的表单数据与数据库进行比较
    username=request.COOKIES.get('username','')
    userLogin = User.objects.filter(username__exact = username)
    if userLogin:
        response = render_to_response('logout.html')
        #清理cookie里保存username
        response.delete_cookie('username')
        return response
    else:
        response = HttpResponseRedirect('/login')
        return response