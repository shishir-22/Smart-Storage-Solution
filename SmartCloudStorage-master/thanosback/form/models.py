from __future__ import unicode_literals
from django.db import models
from django import forms

class Userdata(models.Model):
    user_name=models.CharField(max_length=200,default="")
    email=models.EmailField(max_length=70)
    password = models.CharField(max_length=32,default="qwe")

# class User_url_info(models.Model):
#      userid= models.ForeignKey(Userdata, on_delete=models.CASCADE)
#      url=models.CharField(max_length=200,default="https://www.google.com")
#      subscribers=models.CharField(max_length=800,default="")
#      status=models.CharField(max_length=100 ,default="")
#      access=models.CharField(max_length=10,default="")
#      cron=models.CharField(max_length=10,default="")