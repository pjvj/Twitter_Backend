# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
#from flask import Flask, render_template, request, redirect
from flask import request, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from django.http import HttpResponse
from rest_framework import generics
from .models import UserInfo
from .serializers import UserInfoSerializer
from .forms import UserRegistrationForm
from django.views.decorators.clickjacking import xframe_options_exempt
from django.template import context
#import httplib
#import json
#import http.client
#import random
# Create your views here.


def index(request):
    return render(request, 'api/base.html')
    


#@xframe_options_exempt
def twitter_register(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        if(UserInfo.objects.filter(username=username).exists()):
            print("Nahi ho sakta..already h")
            messages.error(request, 'Username already exists')
            f = UserRegistrationForm()
        else:
            f = UserRegistrationForm(request.POST)
            if f.is_valid():
                f.save()
                messages.success(request, 'Account created successfully')
    else:
        f = UserRegistrationForm()

    return render(request, 'api/register.html', {'form': f})


#@xframe_options_exempt
def twitter_login(request):

    if request.session.has_key('logged_in'):
       username = request.session['logged_in']
       contact = UserInfo.objects.get(username=username)
       print("myname",username)
       return render(request, 'api/homepage.html',{'user':contact})

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        contact = UserInfo.objects.get(username=username,password=password)
        if contact:
            request.session['logged_in'] = username
            return render(request, 'api/homepage.html',{'user':contact})
        else:
            messages.error(request, 'Error wrong username/password')
            form = AuthenticationForm()
        
    else:
        form = AuthenticationForm()
    return render(request, 'api/login.html',{'form':form})

#@xframe_options_exempt
def twitter_home(request):
    
    if request.session.has_key('logged_in'):
       username = request.session['logged_in']
       contact = UserInfo.objects.get(username=username)
       print("again",username)
       return render(request, 'api/homepage.html',{'user':contact})

    else:
        form = AuthenticationForm()
        return render(request, 'api/login.html',{'form':form})
        
    return render(request, 'api/homepage.html',{'user':contact})

#@xframe_options_exempt
def twitter_logout(request):
    try:
        print("bawla bana rahi hai public ka")
        del request.session['logged_in']
        messages.success(request, 'Account logged out successfully')
    except KeyError:
        messages.error(request, 'No account to log out.')
        
    form = AuthenticationForm()
    return render(request, 'api/logout.html')

# view function to display a list of all users...
def users_list(request):
    userslist = UserInfo.objects.all()
    usernames=[]
    for users in userslist:
        usernames.append(users.username)
    return render(request, 'api/users_list.html', {'users': usernames})