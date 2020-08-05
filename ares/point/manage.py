from django.shortcuts import render
import json
import datetime
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
        user1 = user.objects.get(name=username)
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
        sheet1 = wb.sheet_by_index(0)
        list_item_data = sheet1.col_values(0)
        list_gp_data = sheet1.col_values(1)
        list_name_data = sheet1.col_values(2)
        if list_gp_data[0].upper() == "GP":
          loot_data = []
          for i,j,k in zip(list_item_data,list_gp_data,list_name_data):
            if i != "物品":
              url = "https://60.wowfan.net/?search={}&opensearch".format(i)
              response  = requests.get(url).json()
              print(response)
              temp = {'item':response[7][0][1],'name':k,'gp':j}
              loot_data.append(temp)
          # 2020-06-17 21:32:32
          for i in loot_data:
            if score.objects.filter(name=i['name']):
              record.objects.create(item=i['item'],gp=i['gp'],name=i['name'],time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
              score.objects.filter(name=i['name']).update(gp=F('gp')+int(i['gp']))
            else:
              return HttpResponse(i['name']+"名字输入不正确 请检查")


        sheet2 = wb.sheet_by_index(1)
        list_item_data1 = sheet2.col_values(0)
        list_dkp_data = sheet2.col_values(1)
        list_name_data1 = sheet2.col_values(2)
        if list_dkp_data[0].upper() == "DKP":
          loot_data1 = []
          for i,j,k in zip(list_item_data1,list_dkp_data,list_name_data1):
            if i != "物品":
              url = "https://60.wowfan.net/?search={}&opensearch".format(i)
              response  = requests.get(url).json()
              print(response)
              temp = {'item':response[7][0][1],'name':k,'dkp':j}
              loot_data1.append(temp)
          # 2020-06-17 21:32:32
          for i in loot_data1:
            if score.objects.filter(name=i['name']):
              record.objects.create(item=i['item'],dkp=i['dkp'], name=i['name'], time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
              score.objects.filter(name=i['name']).update(dkp=F('dkp')-int(i['dkp']))
            else:
              return HttpResponse(i['name']+"名字输入不正确 请检查")
        #update point_score set gp=0 where gp <0



    else:
      print(obj.errors)
  
  return HttpResponse('OK')
  

def index(request):
  obj = forms.UploadFileForm()
  if not request.session.get('is_login', None):  # 不允许重复登录
    return redirect('/manage/login/')
  return render(request, 'manage/index.html',{'obj':obj})