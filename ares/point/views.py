from django.shortcuts import render,HttpResponse
from .models import DKPadd, DKPtable,player,epgp
import json
from django.db.models import Sum
# Create your views here.
def index(request):
  dkp = DKPtable.objects.all()
  return render(request,'index.html',{'dkp':dkp})

def ajax(request,action):
  #ajax返回epgp列表
  if action == "epgp":
    epgp_score = player.objects.all()
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

  #ajax返回epgp列表
  if action == "epgploot":
    Loot = epgp.objects.filter(gp__isnull=False,item__isnull=False)
    json_list = []
    for i in Loot:
      json_dict = {}
      json_dict["id"] = i.id      
      json_dict["item"] = i.item
      json_dict["gp"] = i.gp
      json_dict["class"] = player.objects.get(name=i.name).job
      json_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
      json_dict["name"] = i.name
      json_list.append(json_dict)
    data ={"data":json_list}
    return HttpResponse(json.dumps(data))

  if action == "epgpaddlog":
    KillLog = epgp.objects.filter(boss__gt="").exclude(ep=0)
    KillLog1 = epgp.objects.filter(boss="衰减10%")
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
    epgp_score = player.objects.all()
    json_list = []
    for i in epgp_score:
      json_dict = {}
      json_dict["class"] = i.job
      DKPadd.objects.extra(where=['"point_dkpadd"."whois" LIKE "'+str(i.name)+',%%") OR ("point_dkpadd"."whois" = "' + str(i.name) +'") OR("point_dkpadd"."whois" LIKE "%%,'+str(i.name)+',%%"']).annotate(dkp_add_sum = Sum("dkp"))
      DKPadd.objects.filter(whois=i.name).annotate(dkp_loot_sum = Sum("dkp"))
      json_dict["dkp"] = dkp_add_sum - dkp_loot_sum
      json_dict["name"] = i.name
      json_list.append(json_dict)
    data ={"data":json_list}
    return HttpResponse(belong)
