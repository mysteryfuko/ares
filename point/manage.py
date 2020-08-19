from django.shortcuts import render
import json
import datetime
from . import models
from django.core import serializers
import os
from django.http import HttpResponse, Http404, FileResponse
from . import forms
from django.shortcuts import redirect
from django.db import connection
import xlrd
import requests,time,zipfile,sqlite3
from django.db.models import F,Q


def login(request):
  if request.session.get('is_login', None):  # 不允许重复登录
    return redirect('manage/index/')
  if request.method == 'POST':
    login_form = forms.UserForm(request.POST)
    message = '请检查填写的内容！'
    if login_form.is_valid():
      username = login_form.cleaned_data.get('username')
      password = login_form.cleaned_data.get('password')
      try:
        user1 = models.user.objects.get(name=username)
      except :
        print(connection.queries)
        message = '用户不存在！'
        return render(request, 'manage/login.html', locals())

      if user1.password == password:
        request.session['is_login'] = True
        request.session['user_name'] = user1.name
        return redirect('/manage/index')
      else:
        message = '密码不正确！'
        return render(request, 'manage/login.html', locals())
    else:
      return render(request, 'manage/login.html', locals())

  login_form = forms.UserForm()
  return render(request, 'manage/login.html', locals())

def do_loot(request):
  if request.method == 'POST':
    obj = forms.UploadFileForm(request.POST, request.FILES)  # 必须填 request.POST

    if obj.is_valid():
      new_loot_file = "./backup/loot/"+ str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())) + ".xls"
      with open(new_loot_file, 'wb') as f:
        for line in obj.cleaned_data['file'].chunks():
          f.write(line)
      f.close()
      #备份
      new_name = "./backup/loot" + str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())) + ".zip"
      zp=zipfile.ZipFile(new_name,'w', zipfile.ZIP_DEFLATED)
      zp.write("db.sqlite3")
      zp.close()

      wb = xlrd.open_workbook(new_loot_file)#打开文件
      for n in wb.sheet_names():
        belong = models.DKPtable.objects.get(name=n).id
        sheet_list = wb.sheet_by_name(n)
        list_item_data = sheet_list.col_values(0)
        list_dkp_data = sheet_list.col_values(1)
        list_name_data = sheet_list.col_values(2)
        if list_dkp_data[0].upper() == "DKP":
          loot_data = []
          for i,j,k in zip(list_item_data,list_dkp_data,list_name_data):
            if i != "物品":
              try:
                url = "https://60.wowfan.net/?search={}&opensearch".format(i)
                response  = requests.get(url).json()
                print(response)
                temp = {'item':response[7][0][1],'name':k,'dkp':j}
                loot_data.append(temp)
              except:
                return HttpResponse(i+"物品输入不正确 请检查")
          for i in loot_data:
            if models.playerDKP.objects.filter(name=i['name']):
              models.DKPLoot.objects.create(item=i['item'],belong=belong,dkp=i['dkp'],Player=i['name'], time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
              models.playerDKP.objects.filter(name=i['name'],belong=belong).update(dkp=F('dkp')-int(i['dkp']))
            else:
              return HttpResponse(i['name']+"名字输入不正确 请检查")         
    else:
      print(obj.errors)
  
  return HttpResponse('OK')
  
def edit(request,act):
  try:
    Name_id = request.GET['id']  
    if act =="add":
      a = models.DKPadd.objects.get(id=Name_id)
      Name_List = models.playerDKP.objects.filter(belong=a.belong).values("name","job").order_by("job")
      a.Player = a.Player.split(',')
      Dkp_list = models.DKPtable.objects.all()
      return render(request,'manage/edite.html',{'dkp':a,'list':Name_List,'Dkp_list':Dkp_list})
    if act =="loot":
      a = models.DKPLoot.objects.get(id=Name_id)  
      return HttpResponse(a)
  except:
    if act =="add":
      try:
        belong = request.GET['belong']
      except:
        belong = 1  
      a = models.DKPadd.objects.get(id=1)
      a.id =""
      a.time = str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
      a.boss = ""
      a.belong = int(belong)
      a.dkp = ""
      a.Player = ""
      Dkp_list = models.DKPtable.objects.all()
      Name_List = models.playerDKP.objects.filter(belong=belong).values("name","job").order_by("job")
      a.Player = a.Player.split(',')
      return render(request,'manage/edite.html',{'dkp':a,'list':Name_List,'Dkp_list':Dkp_list})


  

  

def index(request):
  obj = forms.UploadFileForm()
  if not request.session.get('is_login', None):  # 不允许重复登录
    return redirect('/manage/login/')
  with open('setting.json','r',encoding='utf-8')as fp:
    set_json_data = json.load(fp)
  return render(request, 'manage/index.html',{'obj':obj,"set_json_data":set_json_data})