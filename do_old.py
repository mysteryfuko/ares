# -*- coding:utf-8 -*-
import sqlite3
duoyu = ["泽明","Rz","善孝丶","夜辰","卷卷大魔王","雷先生","天使与恶魔","","Minyuhao","那个奶德","Skywalkeer","刀枪炮","白短短","战神丶雅典娜","能彻斯特方程","你放心我奶你","不良少年今井","落橙橙","蓝色雨天","奶水就是蒩","夜尘","痴情的马库斯","冷血杀戮","随宁","星旭者","红骷髅","荒村尸叔","大米饺子","Straight","人造人十八号","那个奶骑","霜落秋叶","蠢逼","玩儿","魅影之纱","西瓜巨人","名为你的诗","小筱","璃小磊","小法思","无息","阿瑞斯卡妙","playerfidvcm","島根猫","谁便搞搞","老虎钳","宝猪","戳你的屁屁","熊猫会武功","小小玄女","韩大爷","毛布鞋","秋叶","脾气极差","咻咻的仙凤","天蝎座丶灭正","憨逼","你惯的啊","沉睡听风"]

conn = sqlite3.connect('db.sqlite3')
old = sqlite3.connect('old.sqlite3')
old_c = old.cursor()
new_c = conn.cursor()

old_score = old_c.execute("SELECT * from point_score")
for i in old_score:
  if i[1] not in duoyu:
    new_c.execute('INSERT INTO point_playerEPGP (name,job,ep,gp) VALUES (?,?,?,?) ',(i[1],i[2],i[4],i[5]))
    new_c.execute('INSERT INTO point_playerDKP (name,job,dkp,belong) VALUES (?,?,?,?) ',(i[1],i[2],i[3],1))


old_loot = old_c.execute("SELECT * from point_record WHERE item<>0")
for i in old_loot:
  if i[2]:
    new_c.execute('INSERT INTO point_DKPLoot (item,time,belong,Player,dkp) VALUES (?,?,?,?,?) ',(i[1],i[4],1,i[5],i[2]))
  else:
    new_c.execute('INSERT INTO point_epgp (item,gp,time,name) VALUES (?,?,?,?) ',(i[1],i[3],i[4],i[5]))


old_add = old_c.execute("SELECT * from point_record WHERE boss<>0")
for i in old_add:
  if i[6] and i[7] != "衰减10%":
    new_c.execute('INSERT INTO point_epgp (boss,ep,time,name) VALUES (?,?,?,?) ',(i[7],i[6],i[4],i[5]))
    new_c.execute('INSERT INTO point_DKPadd (boss,time,belong,Player,dkp) VALUES (?,?,?,?,?) ',(i[7],i[4],1,i[5],i[2]))
  elif i[7] == "衰减10%":
    new_c.execute('INSERT INTO point_epgp (boss,ep,time,name) VALUES (?,?,?,?) ',(i[7],i[6],i[4],i[5]))
  else:
    new_c.execute('INSERT INTO point_DKPadd (boss,time,belong,Player,dkp) VALUES (?,?,?,?,?) ',(i[7],i[4],1,i[5],i[2]))


conn.commit()


conn.close()
old.close()