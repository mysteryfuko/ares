import requests
import sqlite3
import time
from . import models
import zipfile
from django.db.models import F,Q
import json

class DoReport:
  api_key = "b917de504b076479bf04a6b648be6009"
  startime = 0
  job_dic={}
  def __init__(self,jihe,jiesan):
    self.session = requests.Session()
    self.jihe = []
    self.jiesan = []
    with open('setting.json','r',encoding='utf-8')as fp:
      self.set_json_data = json.load(fp)
    for i in self.set_json_data:
      if i['name'] == "集合分":
        a = 0
        for j in jihe:         
          if j != '0':
            self.jihe.append(i['dkp'][a])
          else:
            self.jihe.append(0)
          a += 1
      elif i['name'] == "解散分":
        a = 0
        for j in jiesan:
          if j != '0':
            self.jiesan.append(i['dkp'][a])
          else:
            self.jiesan.append(0)
          a += 1    

  def get_dahao(self,name):
    try:
      return models.xiaohao.objects.get(xiaohao=name).dahao
    except:
      return name
  
  def get_data(self,url):
    return_data = self.session.get(url)
    return return_data.json()

  def get_fight_data(self,fight_id):
    where_to_do =""
    report_url = "https://www.warcraftlogs.com/v1/report/fights/{}?api_key={}".format(fight_id,self.api_key)
    fight_data = self.get_data(report_url)
    if "status" in fight_data:
      return "ERROR"
    list_data = []
    for i in fight_data['fights']:
      if 'kill' in i and i['boss'] != '0' and i['kill']:
        #生产详细战斗boss及战斗id列表
        temp = {'name':i['name'],'fightID':i['id'],"start_time":i['start_time'],"end_time":i['end_time']}
        list_data.append(temp)

    DataListNum = len(list_data) + 2 #总数据数量

    player_data = []
    temp_name = ""
    player_num = 0
    status_num = 1
    #集合分分析
    for i in fight_data['friendlies']:
      for j in i['fights']:
        if j['id'] == 1:
          temp_name = temp_name + self.get_dahao(i['name'])+","
          player_num += 1       
    temp = {'boss':"集合分",'name':temp_name,'dkp':self.jihe,'time':fight_data['fights'][0]["end_time"]}
    where_to_do += "已完成分析集合分,共计{}人</br>".format(player_num)
    self.set_status(where_to_do,status_num/DataListNum,fight_id)
    player_data.append(temp)


    for k in list_data:
      player_num = 0
      temp_name = ""
      dkpScore = 0  
      for l in self.set_json_data:
        if k['name'] == l['name']:
          dkpScore = l['dkp']

      for i in fight_data['friendlies']:
        if i['type'] != "Boss":
          for j in i['fights']:
            if j['id'] == k['fightID']:
              report_cast = "https://www.warcraftlogs.com:443/v1/report/tables/casts/{}?start={}&end={}&sourceid={}&api_key={}".format(fight_id,k['start_time'],k['end_time'],i['id'],self.api_key)
              cast_data = self.get_data(report_cast)
              if cast_data["entries"]:
                temp_name = temp_name + self.get_dahao(i['name'])+","
                player_num += 1
                self.job_dic[i['name']] = i['type']    
                self.job_dic.update(self.job_dic)
      temp = {'boss':k['name'],'name':temp_name,'dkp':dkpScore,'time':k['end_time']}
      where_to_do += "已完成分析{},共计{}人</br>".format(k['name'],player_num)
      status_num += 1
      self.set_status(where_to_do,status_num/DataListNum,fight_id)
      player_data.append(temp) #{'boss': '鲁西弗隆', 'dkp': 2, 'epgp': 40, 'name': '锤爆诸位的蛋,小悠悠呢,四月你的謊言,剑...rithunter,', 'time': 1049294}

    #全程分分析

    a = len(player_data)
    b = player_data[0]['name'].split(',')
    c = player_data[(a-1)]['name'].split(',')
    all_name= ""
    for i in b:
      if i:
        if i in c:
          all_name = all_name + i +","
    temp = {'boss':"全程分",'name':all_name,'dkp':self.jiesan,'time':player_data[(a-1)]["time"]}
    where_to_do += "已完成分析全程分,共计{}人</br>".format(player_num)
    status_num += 1
    self.set_status(where_to_do,status_num/DataListNum,fight_id)
    player_data.append(temp) 
    self.startime = fight_data['start']
    return player_data

  def BackupData(self):
    new_name = "./backup/report" + str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())) + ".zip"
    zp=zipfile.ZipFile(new_name,'w', zipfile.ZIP_DEFLATED)
    zp.write("db.sqlite3")
    zp.close()

  def WriteData(self,player_data):
    for i in player_data:
      a = time.localtime((int(self.startime)+int(i['time']))/1000.0)
      timenow = time.strftime("%Y-%m-%d %H:%M:%S", a)
      belong = 1
      print(i['dkp'])
      for j in i['dkp']:        
        if j != 0:
          models.DKPadd.objects.create(boss=i['boss'], time=str(timenow),Player= i['name'],dkp=j,belong=belong)
        belong += 1
      name_list = i['name'].split(',')
      for j in name_list:
        belong = 1
        if j :
          for k in i['dkp']:  
            if k != 0:
              if models.playerDKP.objects.filter(name=j,belong=belong):
                models.playerDKP.objects.filter(name=j,belong=belong).update(dkp=F('dkp')+int(k))
              else:
                job =self.job_dic[j].upper()
                models.playerDKP.objects.create(dkp=int(k),name=j,job = job,belong=belong)
            belong += 1

  def set_status(self,status,StatusNum,fight_id): 
    models.status.objects.update_or_create(fight_id=fight_id,defaults={'loading':status,'loadingNum':round(StatusNum,2)})