from django.db import models

# Create your models here.
class score(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=20)
  job = models.CharField(max_length=10)
  dkp = models.IntegerField()
  ep = models.DecimalField(max_digits=10,decimal_places=2)
  gp = models.DecimalField(max_digits=10,decimal_places=2)


class record(models.Model):
  id = models.AutoField(primary_key=True)
  item = models.IntegerField(null=True,blank=True)
  dkp = models.IntegerField(null=True,blank=True)
  gp = models.FloatField(null=True,blank=True)
  time = models.DateTimeField(null=True,blank=True)
  boss = models.CharField(null=True,max_length=40,blank=True)
  name = models.TextField(null=True,blank=True)
  ep = models.FloatField(null=True,blank=True)


class user(models.Model):
  name = models.CharField(max_length=128, unique=True)
  password = models.CharField(max_length=256)

class xiaohao(models.Model):
  dahao = models.CharField(max_length=20)
  xiaohao = models.CharField(max_length=20)