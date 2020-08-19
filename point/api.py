from django.shortcuts import render,HttpResponse
from . import models
import json,time,zipfile,requests
from django.db.models import F,Q
from .report import DoReport

def index(request,act):

  if act =="getitem":
    item = request.POST['item']
    url = "https://60.wowfan.net/?search={}&opensearch".format(item)
    response  = requests.get(url).json()
    json_list = []

    for index in range(len(response[1])):
      temp = {'name':response[1][index],'item':response[7][index][1]}
      print(temp)
      json_list.append(temp)
    return HttpResponse(json.dumps(json_list))


  if act == "SaveAdd":
    data = json.loads(request.POST['data'])
    name_list = json.loads(request.POST['name_list'])
    if data['id']:
      old_list = models.DKPadd.objects.get(id=data['id'])
      for i in old_list.Player.split(','):
        if i :
          models.playerDKP.objects.filter(name=i,belong=old_list.belong).update(dkp=F('dkp')-int(old_list.dkp)) #先减分
      temp_name = ""
      for i in name_list:
        models.playerDKP.objects.filter(name=i,belong=data['belong']).update(dkp=F('dkp')+int(data['dkp'])) #再加分
        temp_name = temp_name + i +","
        
      models.DKPadd.objects.filter(id=data['id']).update(dkp=int(data['dkp']),belong=int(data['belong']),Player=temp_name,boss=data['boss'])
    else:
      temp_name=""
      for i in name_list:
        models.playerDKP.objects.filter(name=i,belong=data['belong']).update(dkp=F('dkp')+int(data['dkp'])) #再加分
        temp_name = temp_name + i +","
      models.DKPadd.objects.create(dkp=int(data['dkp']),belong=int(data['belong']),time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),Player=temp_name,boss=data['boss'])
    return HttpResponse("ok")

  if act == "getaddlist":
    belong = request.POST['belong']
    list_logs = models.DKPadd.objects.filter(belong=belong).order_by('-id').all()[:20]
    json_list = []
    for i in list_logs:
      json_dict = {}
      json_dict["id"] = i.id
      json_dict["boss"] = i.boss
      json_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
      json_dict["player"] = len(i.Player.split(','))-1
      json_list.append(json_dict)
    return HttpResponse(json.dumps(json_list))

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

  if act == "SubmitLoot":
    user = request.POST['user']
    item = request.POST['item']
    dkp = request.POST['dkp']
    belong = request.POST['belong']
    try:
      a=models.playerDKP.objects.get(name=user,belong=belong)
      print(a)
      models.DKPLoot.objects.create(Player=user,item=item,time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),dkp=dkp,belong=belong)
      models.playerDKP.objects.filter(name=user,belong=belong).update(dkp=F('dkp')-int(dkp)) #再加分
    except:
      return HttpResponse("error")
    return HttpResponse("done")

  if act == "setpoint":
    data = request.POST['data']
    try:
      fo = open("setting.json", "w",encoding='utf-8')
      fo.write(data)
      fo.close()
    except BaseException:
      return HttpResponse("error!")
    return HttpResponse("done")

def ajax(request,action):

  if action == "do_status_report":
    url = request.POST['url']
    s = models.status.objects.get(fight_id=url)
    a = []
    a.append(s.loadingNum)
    a.append(s.loading)
    return HttpResponse(json.dumps(a))

  if action =="do_report":
    url = request.POST['url']
    jihe = json.loads(request.POST['jihe'])
    jiesan = json.loads(request.POST['jiesan'])
    try:
      models.status.objects.get(fight_id=url)
      return HttpResponse("ERROR_DONE")
    except:
      p = DoReport(jihe,jiesan)
      PlayerList = p.get_fight_data(url)
      if PlayerList == "ERROR":
        return HttpResponse("ERROR")
      else:
        p.BackupData()
        p.WriteData(PlayerList)
    return HttpResponse("SUCCESS")
  #EPGP衰减
  if action =="do_epgp":
    #备份
    new_name = "./backup/decay" + str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())) + ".zip"
    zp=zipfile.ZipFile(new_name,'w', zipfile.ZIP_DEFLATED)
    zp.write("db.sqlite3")
    zp.close()
    #操作
    models.playerEPGP.objects.update(ep=F('ep')*0.9,gp=((F('gp')+300)*0.9-300))
    models.playerEPGP.objects.filter(Q(gp__lt=0)).update(gp=0)
    decay_name = models.playerEPGP.objects.all()
    decay_name_list = ""
    for i in decay_name:
      decay_name_list = decay_name_list + i.name + ","
    models.epgp.objects.create(boss="衰减10%", time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),name = decay_name_list)
    return HttpResponse("done")
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
        json_dict["class"] = models.playerDKP.objects.get(name=i.Player,belong=belong).job
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
      if i.dkp > 0:
        json_dict["dkp"] = "+"+str(i.dkp)
      else:
        json_dict["dkp"] = i.dkp
      json_dict["active"] = i.boss 
      json_list.append(json_dict)
    for i in loot_logs:
      json_dict = {}
      json_dict["name"] = name   
      json_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
      json_dict["dkp"] = "-"+str(i.dkp)
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
