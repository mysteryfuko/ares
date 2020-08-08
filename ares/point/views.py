from django.shortcuts import render,HttpResponse
from . import models
import json
from django.db.models import Sum
# Create your views here.
def index(request):
  dkp = models.DKPtable.objects.all()
  return render(request,'index.html',{'dkp':dkp})



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