# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    name=models.CharField(max_length=50,default=False)
    username=models.CharField(max_length=50,unique='true')
    password=models.CharField(max_length=30)
    '''
    followers=models.TextField(
        base_field=CharField(max_length=50),
        size=20000000,
        max_length=20000000*51)
    following=models.TextField(base_field=CharField(max_length=50),
    size=20000000,
    max_length=20000000*52)
    '''
