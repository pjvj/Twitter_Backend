# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.

#Model to save the basic informations of the user
class UserInfo(models.Model):
    name=models.CharField(max_length=50,default=False)
    username=models.CharField(max_length=50,unique='true')
    password=models.CharField(max_length=30)
    relationships = models.ManyToManyField('self',through='Relationship',symmetrical=False,related_name='related_to')

    '''
    followers=models.TextField(base_field=CharField(max_length=50),size=20000000,max_length=20000000*51)
    following=models.TextField(base_field=CharField(max_length=50),size=20000000,max_length=20000000*52)
    '''
#class Tweets(models.Model):
class Relationship(models.Model):
	from_person = models.ForeignKey(UserInfo, related_name='from_people')
	to_person = models.ForeignKey(UserInfo, related_name='to_people')