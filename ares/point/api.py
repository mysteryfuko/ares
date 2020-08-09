from django.shortcuts import render,HttpResponse
from . import models
import json

def index(request,act):
  if act == "getsmall":
    small_logs = models.xiaohao.objects.all().order_by('dahao')
    json_list = []
    for i in small_logs:
      json_dict = {}
      json_dict["xiaohao"] = i.xiaohao
      json_dict["dahao"] = i.dahao
      try:
        json_dict["class"] = models.playerDKP.objects.get(name=i.dahao).job
      except BaseException:
        json_dict["class"] = "WARRIOR"
      json_list.append(json_dict)
    return HttpResponse(json.dumps(json_list))

  if act == "getuser":
    user = request.POST['user']
    user_logs = models.playerDKP.objects.filter(name__icontains=user).all().order_by("id").distinct()
    json_list = []
    for i in user_logs:
      json_dict = {}
      json_dict["user"] = i.name
      json_list.append(json_dict)
    return HttpResponse(json.dumps(json_list))

  if act == "submitSmall":
    dahao = request.POST['dahao']
    xiaohao = request.POST['xiaohao']
    try:
      models.playerDKP.objects.get(name=dahao)
      models.xiaohao.objects.create(dahao=dahao,xiaohao=xiaohao)
    except BaseException:
      return HttpResponse("error")
    return HttpResponse("done")

  if act == "setpoint":
    data = request.POST['data']
    try:
      fo = open("setting.json", "w")
      fo.write(data)
      fo.close()
    except BaseException:
      return HttpResponse("error!")
    return HttpResponse("done")

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
      try:
        json_dict["class"] = models.playerEPGP.objects.get(name=i.name).job
      except BaseException:
        json_dict["class"] = "WARRIOR"
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
      json_dict["player"] = len(i.name.split(','))-1
      json_list.append(json_dict)
    for i in KillLog:
      json_dict = {}
      json_dict["id"] = i.id      
      json_dict["boss"] = i.boss
      json_dict["ep"] = i.ep
      json_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
      json_dict["player"] = len(i.name.split(','))-1
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
      json_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
      json_dict["dkp"] = i.dkp
      json_dict["name"] = i.Player
      try:
        json_dict["class"] = models.playerEPGP.objects.get(name=i.Player).job
      except BaseException:
        json_dict["class"] = "WARRIOR"
      json_list.append(json_dict)
    data ={"data":json_list}
    return HttpResponse(json.dumps(data))

  if action =="dkpadd":
    belong = request.GET['belong']
    dkp_add = models.DKPadd.objects.filter(belong=belong).all()
    json_list = []
    for i in dkp_add:
      json_dict = {}
      json_dict["id"] = i.id      
      json_dict["boss"] = i.boss
      json_dict["dkp"] = i.dkp
      json_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
      playerNum = len(i.Player.split(','))-1
      if playerNum == 0:
        playerNum = 1
      json_dict["player"] = playerNum
      json_list.append(json_dict)
    data ={"data":json_list}
    return HttpResponse(json.dumps(data))

  if action =="Playerdkplog":
    belong = request.GET['belong']
    name = request.GET['name']
    loot_logs = models.DKPLoot.objects.filter(belong=belong,Player=name).all()
    logs = models.DKPadd.objects.extra(where=['"point_DKPadd"."belong" ='+belong+' AND "point_DKPadd"."Player" LIKE "'+str(name)+',%%") OR ("point_DKPadd"."belong" ='+belong+' AND "point_DKPadd"."Player" = "' + str(name) +'") OR("point_DKPadd"."belong" ='+belong+' AND "point_DKPadd"."Player" LIKE "%%,'+str(name)+',%%"'])
    json_list = []
    for i in logs:
      json_dict = {}
      json_dict["name"] = name
      json_dict["activeID"] = i.id      
      json_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
      json_dict["dkp"] = i.dkp
      json_dict["active"] = i.boss 
      json_list.append(json_dict)
    for i in loot_logs:
      json_dict = {}
      json_dict["name"] = name   
      json_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
      json_dict["dkp"] = i.dkp
      json_dict["item"] = i.item 
      json_list.append(json_dict)
    data ={"data":json_list}
    return HttpResponse(json.dumps(data))

  if action == "Playerepgplog":
    name = request.GET["name"]
    logs = models.epgp.objects.extra(where=['"point_epgp"."name" LIKE "'+str(name)+',%%") OR ("point_epgp"."name" = "' + str(name) +'") OR("point_epgp"."name" LIKE "%%,'+str(name)+',%%"'])
    json_list = []
    for i in logs:
      json_dict = {}
      json_dict["name"] = name
      json_dict["activeID"] = i.id      
      json_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
      json_dict["ep"] = i.ep
      json_dict["gp"] = i.gp
      json_dict["item"] = i.item 
      json_dict["active"] = i.boss 
      json_list.append(json_dict)
    data ={"data":json_list}

    return HttpResponse(json.dumps(data))