from django.shortcuts import render
from django.http import HttpResponse, Http404, FileResponse
from . import models
import json
from django.db.models import Sum
# Create your views here.
def index(request):
  dkp = models.DKPtable.objects.all()
  return render(request,'index.html',{'dkp':dkp})


def down_dkp(request):
  nameList = models.playerDKP.objects.values('name').distinct()
  table_num = models.DKPtable.objects.all()   
  json_dict = "WebDKP_DkpTable = {\n"
  for i in nameList:
    job = models.playerDKP.objects.filter(name=i['name']).get().job
    if job =="DRUID":
      job = "德鲁伊"
    elif job =="HUNTER":
      job = "猎人"
    elif job =="WARRIOR":
      job = "战士"
    elif job =="ROGUE":
      job = "潜行者"
    elif job =="MAGE":
      job = "法师"
    elif job =="PRIEST":
      job = "牧师"
    elif job =="WARLOCK":
      job = "术士"
    elif job =="PALADIN":
      job = "圣骑士"
    json_dict =json_dict + '["'+i['name']+'"]={\n\t["class"]="'
    json_dict =json_dict + job + '",\n\t["online"]=true,'
    for j in table_num:
      try:
        dkp = models.playerDKP.objects.filter(name=i['name'],belong=j.id).get().dkp         
      except:
        dkp = 0
      if j.id == 1:
        json_dict =json_dict + '\n\t["dkp"]=' + str(dkp) + ',\n'
      json_dict += '\t["dkp_' + str(j.id) + '"]=' + str(dkp) + ',\n\t["dkp_lifetime_' + str(j.id) + '"]=' + str(dkp) + ',\n'
    json_dict += '},\n'
  json_dict = json_dict + '}\nWebDKP_Tables = {\n["BWL"] = {\n		["id"] = 1, \n},\n["TAQ"] = {\n		["id"] = 2, \n},\n}\n\nWebDKP_Loot = {\n}\n\nWebDKP_Alts = {\n}\n\nWebDKP_WebOptions = {\n["ZeroSumEnabled"] = 0,\n\n["CombineAlts"] = 1,\n["TiersEnabled"] = 1,\n["TierSize"] = 50,\n["LifetimeEnabled"] = 1,\n["User"] = "mysteryfuko",\n["AddonVersion"] = 3,\n["WowCatSign"] = "04f91db9576bc71b04a06a3db5e9e4a4",\n}'
  response = FileResponse(json_dict)
  response['content_type'] = "application/octet-stream"
  response['Content-Disposition'] = 'attachment; filename=WebDKP.lua'
  return response

def PlayerDetail(request,name):
  dkp = models.DKPtable.objects.all()
  return render(request,'PlayerDetail.html',{'dkp':dkp,'name':name})

def kill(request,act,bossid):
  point_dkp = 0
  point_ep = 0
  if act =="epgp":
    KillLog = models.epgp.objects.get(id=int(bossid))
    name = KillLog.name.split(',')
    point_ep = KillLog.ep
  elif act =="dkp":
    KillLog = models.DKPadd.objects.get(id=int(bossid))
    name = KillLog.Player.split(',')
    point_dkp = KillLog.dkp
  renderData = {
    "id":bossid,
    "time":KillLog.time,
    "boss":KillLog.boss,
    "ep":point_ep,
    "dkp":point_dkp,
    "name":name
  }
  return render(request,'kill.html',renderData)