from django.shortcuts import render,HttpResponse
from . import models
import json
from django.db.models import Sum
# Create your views here.
def index(request):
  dkp = DKPtable.objects.all()
  return render(request,'index.html',{'dkp':dkp})

def ajax(request,action):
  #ajax返回epgp列表
  if action == "epgp":
    epgp_score = models.playerEPGP.objects.all()
    json_list = []
    for i in epgp_score:
      json_dict = {}
      json_dict["class"] = i.job
      json_dict["ep"] = str(i.ep)
      json_dict["gp"] = str(i.gp)
      json_dict["name"] = i.name
      json_list.append(json_dict)
    data ={"data":json_list}
    return HttpResponse(json.dumps(data))

  #ajax返回epgploot列表
  if action == "epgploot":
    Loot = models.epgp.objects.filter(gp__isnull=False,item__isnull=False)
    json_list = []
    for i in Loot:
      json_dict = {}
      json_dict["id"] = i.id      
      json_dict["item"] = i.item
      json_dict["gp"] = i.gp
      json_dict["class"] = models.playerEPGP.objects.get(name=i.name).job
      json_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
      json_dict["name"] = i.name
      json_list.append(json_dict)
    data ={"data":json_list}
    return HttpResponse(json.dumps(data))

  #ajax返回epgpadd列表
  if action == "epgpaddlog":
    KillLog = models.epgp.objects.filter(boss__gt="").exclude(ep=0)
    KillLog1 = models.epgp.objects.filter(boss="衰减10%")
    json_list = []
    for i in KillLog1:
      json_dict = {}
      json_dict["id"] = i.id      
      json_dict["boss"] = i.boss
      json_dict["ep"] = i.ep
      json_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
      json_dict["player"] = len(i.name.split(',')-1)
      json_list.append(json_dict)
    for i in KillLog:
      json_dict = {}
      json_dict["id"] = i.id      
      json_dict["boss"] = i.boss
      json_dict["ep"] = i.ep
      json_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
      json_dict["player"] = len(i.name.split(',')-1)
      json_list.append(json_dict)
    data ={"data":json_list}
    return HttpResponse(json.dumps(data))

  if action == "dkp":
    belong = request.GET['belong']
    dkp_score = models.playerDKP.objects.filter(belong=belong).all()
    json_list = []
    for i in dkp_score:
      json_dict = {}
      json_dict["class"] = i.job
      json_dict["dkp"] = i.dkp
      json_dict["name"] = i.name
      json_list.append(json_dict)
    data ={"data":json_list}
    return HttpResponse(json.dumps(data))

  if action == "dkploot":
    belong = request.GET['belong']
    dkp_loot = models.DKPLoot.objects.filter(belong=belong).all()
    json_list = []
    for i in dkp_loot:
      json_dict = {}
      json_dict["item"] = i.item
      json_dict["time"] = i.time
      json_dict["dkp"] = i.dkp
      json_dict["name"] = i.name
      json_dict["class"] = i.job
      json_list.append(json_dict)
    data ={"data":json_list}
    return HttpResponse(json.dumps(data))
