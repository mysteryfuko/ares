from django.shortcuts import render
from .models import score,record,user
import json
import datetime
from django.core import serializers
import os
from django.http import HttpResponse, Http404, FileResponse
import time
from point import do_report
from django.db.models import F,Q
import zipfile

from django.db import connection

def index(request):
    return render(request,'index.html')

def ajax(request,action):
  global where_to_do,num
  if action =="do_epgp":
    #备份
    new_name = "./backup/decay" + str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())) + ".zip"
    zp=zipfile.ZipFile(new_name,'w', zipfile.ZIP_DEFLATED)
    zp.write("db.sqlite3")
    zp.close()
    #操作
    epgp = score.objects.update(ep=F('ep')*0.9,gp=((F('gp')+300)*0.9-300))
    epgp1 = score.objects.filter(Q(gp__lt=0)).update(gp=0)
    decay_name = score.objects.all()
    decay_name_list = ""
    for i in decay_name:
      decay_name_list = decay_name_list + i.name + ","
    record.objects.create(boss="衰减10%", time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),name = decay_name_list,ep=0,gp=0,dkp=0)
    return HttpResponse("done")

  if action == "do_report":
    url = request.POST["url"]
    print(url)
    if do_report.list_num == 1:
      do_report.where_to_do="开始分析"
      do_report.num = 0
      detail_list = do_report.get_fight_data(url)
    do_report.list_num = 1
    return HttpResponse(detail_list)

  if action == "do_status_report":
    dic = [(do_report.num/do_report.list_num)*100,do_report.where_to_do]
    return HttpResponse(json.dumps(dic))

  #ajax返回epgp列表
  if action == "epgp":
    epgp = score.objects.all()
    json_list = []
    for i in epgp:
      json_dict = {}
      json_dict["class"] = i.job
      json_dict["ep"] = str(i.ep)
      json_dict["gp"] = str(i.gp)
      json_dict["name"] = i.name
      json_list.append(json_dict)
    data ={"data":json_list}
    return HttpResponse(json.dumps(data))
  
  #ajax返回dkp列表
  if action == "dkp": 
    epgp = score.objects.all()
    json_list = []
    for i in epgp:
      json_dict = {}
      json_dict["class"] = i.job
      json_dict["dkp"] = i.dkp
      json_dict["name"] = i.name
      json_list.append(json_dict)
    data ={"data":json_list}
    return HttpResponse(json.dumps(data))

  #ajax返回epgp loot记录
  if action == "epgplootlog":
    KillLog = record.objects.filter(gp__isnull=False,item__isnull=False)
    json_list = []
    for i in KillLog:
      json_dict = {}
      json_dict["id"] = i.id      
      json_dict["item"] = i.item
      json_dict["gp"] = i.gp
      json_dict["class"] = score.objects.get(name=i.name).job
      json_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
      json_dict["name"] = i.name
      json_list.append(json_dict)
    data ={"data":json_list}
    return HttpResponse(json.dumps(data))

    #ajax返回总ep奖励记录 {,"ep":"22","player":"18404","},
  if action == "epgpaddlog":
    KillLog = record.objects.filter(boss__gt="").exclude(ep=0)
    KillLog1 = record.objects.filter(boss="衰减10%")
    json_list = []
    for i in KillLog1:
      json_dict = {}
      json_dict["id"] = i.id      
      json_dict["boss"] = i.boss
      json_dict["ep"] = i.ep
      json_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
      json_dict["player"] = len(i.name.split(','))
      json_list.append(json_dict)
    for i in KillLog:
      json_dict = {}
      json_dict["id"] = i.id      
      json_dict["boss"] = i.boss
      json_dict["ep"] = i.ep
      json_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
      json_dict["player"] = len(i.name.split(','))
      json_list.append(json_dict)
    data ={"data":json_list}
    return HttpResponse(json.dumps(data))

    #ajax返回dkp loot记录
  if action == "dkplootlog":
    KillLog = record.objects.filter(dkp__isnull=False,item__isnull=False)
    json_list = []
    for i in KillLog:
      json_dict = {}
      json_dict["id"] = i.id      
      json_dict["item"] = i.item
      json_dict["dkp"] = i.dkp
      json_dict["class"] = score.objects.get(name=i.name).job
      json_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
      json_dict["name"] = i.name
      json_list.append(json_dict)
    data ={"data":json_list}
    return HttpResponse(json.dumps(data))
    

      #ajax返回总dkp奖励记录
  if action == "dkpaddlog":
    KillLog = record.objects.filter(dkp__gt=0,boss__gt="")
    json_list = []
    for i in KillLog:
      json_dict = {}
      json_dict["id"] = i.id      
      json_dict["name"] = i.boss
      json_dict["dkp"] = i.dkp
      json_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
      json_dict["player"] = len(i.name.split(','))
      json_list.append(json_dict)
    data ={"data":json_list}

    return HttpResponse(json.dumps(data))


  if action == "Playerepgplog":
    name = request.GET["name"]
    logs = record.objects.extra(where=['("point_record"."ep" <> 0 AND "point_record"."name" LIKE "'+str(name)+',%%") OR ("point_record"."ep" <> 0 AND "point_record"."name" = "' + str(name) +'") OR ("point_record"."ep" <> 0 AND "point_record"."name" LIKE "%%,'+str(name)+',%%") OR ("point_record"."gp" <> 0 AND "point_record"."name" LIKE "'+str(name)+',%%") OR ("point_record"."gp" <> 0 AND "point_record"."name" = "' + str(name) +'") OR ("point_record"."gp" <> 0 AND "point_record"."name" LIKE "%%,'+str(name)+',%%") OR ("point_record"."ep" = 0 AND "point_record"."GP" = 0 AND "point_record"."dkp" = 0 AND "point_record"."name" LIKE "'+str(name)+',%%") OR ("point_record"."ep" = 0 AND "point_record"."GP" = 0 AND "point_record"."dkp" = 0 AND "point_record"."name" = "' + str(name) +'") OR ("point_record"."ep" = 0 AND "point_record"."GP" = 0 AND "point_record"."dkp" = 0 AND "point_record"."name" LIKE "%%,'+str(name)+',%%")'])
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

  if action == "Playerdkplog":
    name = request.GET["name"]
    nameid = score.objects.get(name=name).id
    logs = record.objects.extra(where=['"point_record"."dkp" <> 0 AND "point_record"."name" LIKE "'+str(name)+',%%") OR ("point_record"."dkp" <> 0 AND "point_record"."name" = "' + str(name) +'") OR("point_record"."dkp" <> 0 AND "point_record"."name" LIKE "%%,'+str(name)+',%%"'])
    json_list = []
    for i in logs:
      json_dict = {}
      json_dict["name"] = name
      json_dict["activeID"] = i.id      
      json_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
      json_dict["dkp"] = i.dkp
      json_dict["item"] = i.item 
      json_dict["active"] = i.boss 
      json_list.append(json_dict)
    data ={"data":json_list}
    return HttpResponse(json.dumps(data))

def PlayerDetail(request,name):
  return render(request,'PlayerDetail.html',{"name":name})

  
def kill(request,bossid):
  KillLog = record.objects.get(id=int(bossid))
  name = KillLog.name.split(',')
  renderData = {
    "id":bossid,
    "time":KillLog.time,
    "boss":KillLog.boss,
    "ep":KillLog.ep,
    "dkp":KillLog.dkp,
    "name":name
  }
  #print(renderData)
  return render(request,'kill.html',renderData)

def down_dkp(request):
  epgp = score.objects.all()
  json_dict = "WebDKP_DkpTable = {\n"
  for i in epgp:
    if i.job =="DRUID":
      job = "德鲁伊"
    elif i.job =="HUNTER":
      job = "猎人"
    elif i.job =="WARRIOR":
      job = "战士"
    elif i.job =="ROGUE":
      job = "潜行者"
    elif i.job =="MAGE":
      job = "法师"
    elif i.job =="PRIEST":
      job = "牧师"
    elif i.job =="WARLOCK":
      job = "术士"
    elif i.job =="PALADIN":
      job = "圣骑士"
    json_dict =json_dict + '["'+i.name+'"]={\n\t["class"]="'
    json_dict =json_dict + job + '",\n\t["online"]=true,\n\t["dkp"]='
    json_dict= json_dict + str(i.dkp) + ',\n\t["dkp_1"]=' +str(i.dkp)+',\n\t["dkp_lifetime_1"]='+str(i.dkp)+',\n},\n'
  json_dict = json_dict + '}\nWebDKP_Tables = {\n["BWL"] = {\n		["id"] = 1, \n},\n}\n\nWebDKP_Loot = {\n}\n\nWebDKP_Alts = {\n}\n\nWebDKP_WebOptions = {\n["ZeroSumEnabled"] = 0,\n\n["CombineAlts"] = 1,\n["TiersEnabled"] = 1,\n["TierSize"] = 50,\n["LifetimeEnabled"] = 1,\n["User"] = "mysteryfuko",\n["AddonVersion"] = 3,\n["WowCatSign"] = "04f91db9576bc71b04a06a3db5e9e4a4",\n}'
  response = FileResponse(json_dict)
  response['content_type'] = "application/octet-stream"
  response['Content-Disposition'] = 'attachment; filename=WebDKP.lua'
  return response


def down_epgp(request):
  epgp = score.objects.all()
  epgp_str = 'AirjEPGPDB = {\
  ["profileKeys"] = {\
    ["明明是女孩子 - 怀特迈恩"] = "Default",\
  },\
  ["profiles"] = {\
    ["Default"] = {\
      ["lastTimerTime"] = 1593536549,\
      ["log"] = {\
      },\
      ["settings"] = {\
        ["log_gp"] = true,\
        ["points_WARRIOR"] = true,\
        ["points_HUNTER"] = true,\
        ["itemGpDoubleLevel"] = 10,\
        ["points_massReason"] = "test",\
        ["points_DRUID"] = true,\
        ["settings_profile"] = "default",\
        ["points_massAmount"] = "1",\
        ["itemBaseGp"] = 1000,\
        ["log_ep"] = true,\
        ["points_ROGUE"] = true,\
        ["points_MAGE"] = true,\
        ["points_SHAMAN"] = true,\
        ["log_undone"] = true,\
        ["points_PRIEST"] = true,\
        ["points_WARLOCK"] = true,\
        ["points_PALADIN"] = true,\
      },\
      ["standbys"] = {\
      },\
      ["profiles"] = {\
        {\
          ["logs"] = {\
            {\
            },\
          },\
          ["name"] = "MC",\
          ["settings"] = {\
            ["BASE_GP"] = "300",\
            ["DECAY_P"] = "10",\
            ["EXTRAS_P"] = "0",\
            ["MASS_EP"] = "1",\
            ["MIN_EP"] = "0",\
          },\
          ["points"] = {'
  for i in epgp:
    temp = '["{}"] = {{\
            ["gp"] = {},\
            ["name"] = "{}",\
            ["ep"] = {},\
          }},'.format(i.name,i.gp,i.name,i.ep)
    epgp_str += temp
  epgp_str = epgp_str + '},\
              ["altData"] = {\
              },\
              ["gearPoints"] = {					\
                [16901] = {\
                  ["point"] = 360,\
                  ["itemId"] = 16901,\
                },\
                [18814] = {\
                  ["point"] = 300,\
                  ["itemId"] = 18814,\
                },\
                [18423] = {\
                  ["point"] = 340,\
                  ["itemId"] = 18423,\
                },\
                [18806] = {\
                  ["point"] = 230,\
                  ["itemId"] = 18806,\
                },\
                [18808] = {\
                  ["point"] = 150,\
                  ["itemId"] = 18808,\
                },\
                [18810] = {\
                  ["offPoint"] = 240,\
                  ["point"] = 240,\
                  ["itemId"] = 18810,\
                },\
                [18812] = {\
                  ["point"] = 160,\
                  ["itemId"] = 18812,\
                },\
                [16909] = {\
                  ["point"] = 360,\
                  ["itemId"] = 16909,\
                },\
                [18816] = {\
                  ["point"] = 560,\
                  ["itemId"] = 18816,\
                },\
                [16810] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16810,\
                },\
                [18820] = {\
                  ["point"] = 320,\
                  ["itemId"] = 18820,\
                },\
                [16939] = {\
                  ["point"] = 360,\
                  ["itemId"] = 16939,\
                },\
                [17078] = {\
                  ["point"] = 160,\
                  ["itemId"] = 17078,\
                },\
                [16921] = {\
                  ["point"] = 360,\
                  ["itemId"] = 16921,\
                },\
                [16796] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16796,\
                },\
                [18703] = {\
                  ["point"] = 800,\
                  ["itemId"] = 18703,\
                },\
                [18832] = {\
                  ["point"] = 400,\
                  ["itemId"] = 18832,\
                },\
                [16929] = {\
                  ["point"] = 360,\
                  ["itemId"] = 16929,\
                },\
                [16861] = {\
                  ["point"] = 140,\
                  ["itemId"] = 16861,\
                },\
                [19145] = {\
                  ["point"] = 320,\
                  ["itemId"] = 19145,\
                },\
                [18205] = {\
                  ["point"] = 240,\
                  ["itemId"] = 18205,\
                },\
                [18842] = {\
                  ["offPoint"] = 333,\
                  ["point"] = 620,\
                  ["itemId"] = 18842,\
                },\
                [17066] = {\
                  ["offPoint"] = 536,\
                  ["point"] = 180,\
                  ["itemId"] = 17066,\
                },\
                [16814] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16814,\
                },\
                [16816] = {\
                  ["offPoint"] = 210,\
                  ["point"] = 210,\
                  ["itemId"] = 16816,\
                },\
                [17072] = {\
                  ["point"] = 360,\
                  ["itemId"] = 17072,\
                },\
                [16820] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16820,\
                },\
                [17076] = {\
                  ["point"] = 660,\
                  ["itemId"] = 17076,\
                },\
                [16824] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16824,\
                },\
                [16826] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16826,\
                },\
                [16955] = {\
                  ["point"] = 360,\
                  ["itemId"] = 16955,\
                },\
                [16857] = {\
                  ["point"] = 140,\
                  ["itemId"] = 16857,\
                },\
                [18878] = {\
                  ["point"] = 200,\
                  ["itemId"] = 18878,\
                },\
                [16834] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16834,\
                },\
                [16963] = {\
                  ["point"] = 360,\
                  ["itemId"] = 16963,\
                },\
                [16853] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16853,\
                },\
                [17105] = {\
                  ["point"] = 240,\
                  ["itemId"] = 17105,\
                },\
                [16849] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16849,\
                },\
                [18879] = {\
                  ["point"] = 210,\
                  ["itemId"] = 18879,\
                },\
                [16846] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16846,\
                },\
                [16848] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16848,\
                },\
                [16850] = {\
                  ["point"] = 140,\
                  ["itemId"] = 16850,\
                },\
                [19138] = {\
                  ["point"] = 150,\
                  ["itemId"] = 19138,\
                },\
                [16854] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16854,\
                },\
                [19142] = {\
                  ["point"] = 270,\
                  ["itemId"] = 19142,\
                },\
                [16858] = {\
                  ["point"] = 140,\
                  ["itemId"] = 16858,\
                },\
                [19146] = {\
                  ["point"] = 150,\
                  ["itemId"] = 19146,\
                },\
                [16862] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16862,\
                },\
                [16864] = {\
                  ["point"] = 140,\
                  ["itemId"] = 16864,\
                },\
                [16866] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16866,\
                },\
                [18646] = {\
                  ["point"] = 700,\
                  ["itemId"] = 18646,\
                },\
                [17102] = {\
                  ["point"] = 150,\
                  ["itemId"] = 17102,\
                },\
                [19140] = {\
                  ["point"] = 240,\
                  ["itemId"] = 19140,\
                },\
                [16856] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16856,\
                },\
                [19136] = {\
                  ["point"] = 360,\
                  ["itemId"] = 19136,\
                },\
                [17107] = {\
                  ["point"] = 160,\
                  ["itemId"] = 17107,\
                },\
                [16835] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16835,\
                },\
                [16868] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16868,\
                },\
                [16860] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16860,\
                },\
                [16829] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16829,\
                },\
                [16954] = {\
                  ["point"] = 360,\
                  ["itemId"] = 16954,\
                },\
                [17110] = {\
                  ["offPoint"] = 100,\
                  ["point"] = 100,\
                  ["itemId"] = 17110,\
                },\
                [18805] = {\
                  ["point"] = 460,\
                  ["itemId"] = 18805,\
                },\
                [16821] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16821,\
                },\
                [16938] = {\
                  ["point"] = 360,\
                  ["itemId"] = 16938,\
                },\
                [17071] = {\
                  ["point"] = 240,\
                  ["itemId"] = 17071,\
                },\
                [16900] = {\
                  ["point"] = 360,\
                  ["itemId"] = 16900,\
                },\
                [17069] = {\
                  ["offPoint"] = 616,\
                  ["point"] = 420,\
                  ["itemId"] = 17069,\
                },\
                [18809] = {\
                  ["point"] = 160,\
                  ["itemId"] = 18809,\
                },\
                [18811] = {\
                  ["point"] = 150,\
                  ["itemId"] = 18811,\
                },\
                [17067] = {\
                  ["point"] = 120,\
                  ["itemId"] = 17067,\
                },\
                [17065] = {\
                  ["point"] = 220,\
                  ["itemId"] = 17065,\
                },\
                [18817] = {\
                  ["point"] = 360,\
                  ["itemId"] = 18817,\
                },\
                [16914] = {\
                  ["point"] = 360,\
                  ["itemId"] = 16914,\
                },\
                [18821] = {\
                  ["offPoint"] = 210,\
                  ["point"] = 210,\
                  ["itemId"] = 18821,\
                },\
                [18823] = {\
                  ["point"] = 220,\
                  ["itemId"] = 18823,\
                },\
                [16795] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16795,\
                },\
                [16922] = {\
                  ["point"] = 360,\
                  ["itemId"] = 16922,\
                },\
                [16797] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16797,\
                },\
                [16803] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16803,\
                },\
                [16801] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16801,\
                },\
                [16930] = {\
                  ["point"] = 360,\
                  ["itemId"] = 16930,\
                },\
                [16805] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16805,\
                },\
                [16807] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16807,\
                },\
                [17063] = {\
                  ["point"] = 300,\
                  ["itemId"] = 17063,\
                },\
                [16811] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16811,\
                },\
                [16813] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16813,\
                },\
                [16815] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16815,\
                },\
                [16817] = {\
                  ["offPoint"] = 140,\
                  ["point"] = 140,\
                  ["itemId"] = 16817,\
                },\
                [16819] = {\
                  ["point"] = 140,\
                  ["itemId"] = 16819,\
                },\
                [17075] = {\
                  ["point"] = 480,\
                  ["itemId"] = 17075,\
                },\
                [16823] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16823,\
                },\
                [16825] = {\
                  ["point"] = 140,\
                  ["itemId"] = 16825,\
                },\
                [16827] = {\
                  ["point"] = 140,\
                  ["itemId"] = 16827,\
                },\
                [18861] = {\
                  ["point"] = 240,\
                  ["itemId"] = 18861,\
                },\
                [16831] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16831,\
                },\
                [16833] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16833,\
                },\
                [16962] = {\
                  ["point"] = 360,\
                  ["itemId"] = 16962,\
                },\
                [16851] = {\
                  ["point"] = 140,\
                  ["itemId"] = 16851,\
                },\
                [16800] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16800,\
                },\
                [16852] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16852,\
                },\
                [18875] = {\
                  ["point"] = 260,\
                  ["itemId"] = 18875,\
                },\
                [16845] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16845,\
                },\
                [16847] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16847,\
                },\
                [17103] = {\
                  ["point"] = 620,\
                  ["itemId"] = 17103,\
                },\
                [19137] = {\
                  ["point"] = 200,\
                  ["itemId"] = 19137,\
                },\
                [19139] = {\
                  ["point"] = 240,\
                  ["itemId"] = 19139,\
                },\
                [17109] = {\
                  ["offPoint"] = 200,\
                  ["point"] = 200,\
                  ["itemId"] = 17109,\
                },\
                [19143] = {\
                  ["point"] = 220,\
                  ["itemId"] = 19143,\
                },\
                [16859] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16859,\
                },\
                [19147] = {\
                  ["point"] = 210,\
                  ["itemId"] = 19147,\
                },\
                [16863] = {\
                  ["point"] = 210,\
                  ["itemId"] = 16863,\
                },\
                [16865] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16865,\
                },\
                [16867] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16867,\
                },\
                [16802] = {\
                  ["point"] = 140,\
                  ["itemId"] = 16802,\
                },\
                [16798] = {\
                  ["point"] = 280,\
                  ["itemId"] = 16798,\
                },\
              },\
            }, \
            ["default"] = {\
              ["logs"] = {\
              },\
              ["name"] = "Officer Note",\
              ["points"] = {\
              },\
              ["altData"] = {\
              },\
              ["settings"] = {\
                ["points_MAGE"] = true,\
                ["points_WARRIOR"] = true,\
                ["points_SHAMAN"] = true,\
                ["itemBaseGp"] = 1000,\
                ["points_HUNTER"] = true,\
                ["points_PALADIN"] = true,\
                ["points_WARLOCK"] = true,\
                ["points_ROGUE"] = true,\
                ["itemGpDoubleLevel"] = 10,\
                ["points_massReason"] = "test",\
                ["points_DRUID"] = true,\
                ["points_PRIEST"] = true,\
                ["settings_profile"] = "1",\
                ["points_massAmount"] = "1",\
              },\
              ["gearPoints"] = {\
              },\
            },\
          },\
          ["onlineTimes"] = {\
            ["明明是女孩子"] = 1593536494,\
            ["西瓜巨人"] = 1593536445,\
          },\
          ["assigns"] = {\
          },\
          ["gearPoints"] = {\
            [18564] = {\
              ["point"] = 3958,\
              ["itemId"] = 18564,\
            },\
            [18705] = {\
              ["point"] = 2799,\
              ["itemId"] = 18705,\
            },\
            [17204] = {\
              ["point"] = 10556,\
              ["itemId"] = 17204,\
            },\
            [18563] = {\
              ["point"] = 3958,\
              ["itemId"] = 18563,\
            },\
            [18646] = {\
              ["point"] = 3732,\
              ["itemId"] = 18646,\
            },\
            [18703] = {\
              ["point"] = 2799,\
              ["itemId"] = 18703,\
            },\
            [18423] = {\
              ["point"] = 975,\
              ["itemId"] = 18423,\
            },\
          },\
        },\
      },\
    }'
  response = FileResponse(epgp_str)
  response['content_type'] = "application/octet-stream"
  response['Content-Disposition'] = 'attachment; filename=AirjEPGP.lua'
  return response

