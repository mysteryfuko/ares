import requests
import sqlite3
from retrying import retry
import time
from .models import score,record,xiaohao
import zipfile
from django.db.models import F,Q
import json


api_key = "b917de504b076479bf04a6b648be6009"
with open('setting.json','r')as fp:
  set_json_data = json.load(fp)

where_to_do = ""
num = 0
list_num = 1
session = requests.Session()

def get_data(url):
  return_data = session.get(url)
  return return_data.json()

def get_dahao(name):
  user_log = xiaohao.objects.filter(xiaohao=name)
  if user_log:
    user_log = xiaohao.objects.get(xiaohao=name)
    return user_log.dahao
  else:
    return name

""" Send a request to wcl
:param fight_id: the special id for WCL
:return dict list_data,boss_list
:rtype:list_data['name'] the boss name
:rtype:list_data['fightID'] the ID for the fight
:rtype:list_data['star_time'] the fight startime
:rtype:list_data['end_time'] the fight endtime
:
"""
def get_fight_data(fight_id):
  global where_to_do,num,list_num
  report_url = "https://www.warcraftlogs.com/v1/report/fights/{}?api_key={}".format(fight_id,api_key)
  fight_data = get_data(report_url)
  if "status" in fight_data:
    return "ERROR"
  list_data = []
  for i in fight_data['fights']:
    if 'kill' in i and i['boss'] != '0' and i['kill']:
      #生产详细战斗boss及战斗id列表
      temp = {'name':i['name'],'fightID':i['id'],"start_time":i['start_time'],"end_time":i['end_time']}
      list_data.append(temp)  #{'end_time': 1049294, 'fightID': 10, 'name': '鲁西弗隆', 'start_time': 968847}
  list_num = len(list_data)
  
  player_data = []
  temp_name = ""
  player_num = 0
  #集合分分析
  for i in fight_data['friendlies']:
    for j in i['fights']:
      if j['id'] == 1:
        temp_name = temp_name + get_dahao(i['name'])+","
        player_num += 1       
  temp = {'boss':"集合分",'name':temp_name,'epgp':50,'dkp':5,'time':fight_data['fights'][0]["end_time"]}
  where_to_do = "已完成分析集合分,共计{}人".format(player_num)
  player_data.append(temp)


  temp_dic = {}
  for k in list_data:
    player_num = 0
    temp_name = ""
    epgpScore = 0
    dkpScore = 0  
    for m in epgp:
      if k['name'] == m['name']:
        epgpScore = m['point']
    for l in dkp:
      if k['name'] == l['name']:
        dkpScore = l['point']

    for i in fight_data['friendlies']:
      if i['type'] != "Boss":
        for j in i['fights']:
          if j['id'] == k['fightID']:
            report_cast = "https://www.warcraftlogs.com:443/v1/report/tables/casts/{}?start={}&end={}&sourceid={}&api_key={}".format(fight_id,k['start_time'],k['end_time'],i['id'],api_key)
            cast_data = get_data(report_cast)
            if cast_data["entries"]:
              temp_name = temp_name + get_dahao(i['name'])+","
              player_num += 1
              temp_dic[i['name']] = i['type']    
              temp_dic.update(temp_dic)          
    temp = {'boss':k['name'],'name':temp_name,'epgp':epgpScore,'dkp':dkpScore,'time':k['end_time']}
    num = num + 1
    where_to_do = "已完成分析{},共计{}人".format(k['name'],player_num)
    print("已完成分析{}".format(k['name'])) 
    print(num)
    print(where_to_do)
    player_data.append(temp) #{'boss': '鲁西弗隆', 'dkp': 2, 'epgp': 40, 'name': '锤爆诸位的蛋,小悠悠呢,四月你的謊言,剑...rithunter,', 'time': 1049294}

  #全程分分析
  where_to_do = "正在分析全程分"
  a = len(player_data)
  b = player_data[0]['name'].split(',')
  c = player_data[(a-1)]['name'].split(',')
  all_name= ""
  for i in b:
    if i:
      if i in c:
        all_name = all_name + i +","
  temp = {'boss':"全程分",'name':all_name,'epgp':40,'dkp':5,'time':player_data[(a-1)]["time"]}
  where_to_do = "已完成分析集合分,共计{}人".format(player_num)
  player_data.append(temp) 



  where_to_do = "正在写入数据"
  #备份
  new_name = "./backup/report" + str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())) + ".zip"
  zp=zipfile.ZipFile(new_name,'w', zipfile.ZIP_DEFLATED)
  zp.write("db.sqlite3")
  zp.close()

  for i in player_data:
    a = time.localtime((int(fight_data['start'])+int(i['time']))/1000.0)
    timenow = time.strftime("%Y-%m-%d %H:%M:%S", a)
    record.objects.create(boss=i['boss'], time=str(timenow),name = i['name'],ep=i['epgp'],dkp=i['dkp'])
    nameall = i['name'].split(',')
    for j in nameall:
      if j :       
        if score.objects.filter(name=j):
          score.objects.filter(name=j).update(ep=F('ep')+int(i['epgp']),dkp=F('dkp')+int(i['dkp']))
        else:
          a = temp_dic[j].upper()
          score.objects.create(dkp=int(i['dkp']), ep=int(i['epgp']), name=j,job = a,gp=0)

  return player_data

      


