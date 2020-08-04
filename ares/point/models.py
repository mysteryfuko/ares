from django.db import models

# Create your models here.
class playerEPGP(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=20)
  job = models.CharField(max_length=10,default="WARRIOR")
  ep = models.DecimalField(max_digits=8,decimal_places=2)
  gp = models.DecimalField(max_digits=8,decimal_places=2)

class epgp(models.Model):
  id = models.AutoField(primary_key=True)
  item = models.IntegerField(null=True)
  ep = models.FloatField(null=True,blank=True)
  gp = models.FloatField(null=True,blank=True)
  time = models.DateTimeField()
  boss = models.CharField(null=True,max_length=40,blank=True)
  name = models.TextField(null=True)

class DKPtable(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=20)

class playerDKP(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=20)
  job = models.CharField(max_length=10,default="WARRIOR")
  dkp = models.IntegerField()
  belong = models.IntegerField()

class DKPLoot(models.Model):
  time = models.DateTimeField()
  item = models.IntegerField()
  belong = models.IntegerField()
  Player = models.TextField()
  dkp = models.IntegerField()
  
class DKPadd(models.Model):
  time = models.DateTimeField()
  boss = models.TextField()
  belong = models.IntegerField()
  Player = models.TextField()
  dkp = models.IntegerField()

class user(models.Model):
  name = models.CharField(max_length=128, unique=True)
  password = models.CharField(max_length=256)

class xiaohao(models.Model):
  dahao = models.CharField(max_length=20)
  xiaohao = models.CharField(max_length=20)