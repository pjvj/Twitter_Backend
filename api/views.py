# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
#from flask import Flask, render_template, request, redirect
from flask import request, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

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
#import httplib
#import json
#import http.client
#import random

# Create your views here.
'''
class UserRetrieval(APIView):
     def post(self, request, format=None):
        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserValidate(APIView):

     def logout(self,request):
         try:
             del request.session['username']
         except:
             pass
         return Response("<strong>You are logged out.</strong>")

     def post(self, request, format=None):
        #session_username=""
        if request.session.has_key('username'):
            session_username = request.session['username']
            contact_of_session_username = UserInfo.objects.filter(username=username)
            password_of_session_username = contact_of_session_username.password
            #rem_time=request.session.get_expiry_age()
            username=session_username
            password=password_of_session_username
        else:
            username = request.data['username']
            password = request.data['password']
        if username and password:
            contact = UserInfo.objects.get(username=username,password=password)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if contact:
            serializer = UserInfoSerializer(contact)
            request.session['username'] = username
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

'''

def index(request):
    return render(request, 'api/base.html')
    #return HttpResponse("Hello there")

@xframe_options_exempt
def register(request):
    if request.method == 'POST':
        f = UserRegistrationForm(request.POST)
        if f.is_valid():
            userObj = f.cleaned_data
            name=userObj['name']
            username = userObj['username']
            password =  userObj['password']
            if not (UserInfo.objects.filter(username=username).exists()) :
                #user=UserInfo.objects.create(name,username, password)
                #user = authenticate(username = username, password = password)
                #user=f.save(commit=False)
                #user.save()
                f.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')
    else:
        f = UserRegistrationForm()

    return render(request, 'api/register.html', {'form': f})

@xframe_options_exempt
def twitter_login(request):
    '''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            contact = UserInfo.objects.get(username=username,password=password)
            request.session['logged_in'] = username
            #return render(request, 'api/homepage.html',{'user':contact})
            return redirect('twitter_home')
        else:
            messages.error(request, 'Error wrong username/password')
    '''
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            username = request.POST.get('username')
            request.session['logged_in'] = username
            return redirect('twitter_home')
        else:
            messages.error(request, 'Error wrong username/password')
    else:
        form = AuthenticationForm()
    return render(request, 'api/login.html',{'form':form,'messages':messages})

        #return render(request, 'api/homepage.html',{'user':contact})
@xframe_options_exempt
def twitter_home(request):
    #if not request.session.get('logged_in'):
        #return render(request, 'api/login.html')
    if 'logged_in' not in request.session:
    #if not request.session['logged_in']:
        return render(request, 'api/login.html')
        #return redirect('twitter_login')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            contact = UserInfo.objects.get(username=username,password=password)
    return render(request, 'api/homepage.html',{'user':contact})

@xframe_options_exempt
def twitter_logout(request):
    try:
        del request.session['logged_in']
        messages.success(request, 'Account logged out successfully')
    except KeyError:
        return redirect('twitter_login')
    return render(request, 'api/login.html',{'messages':messages})

# view function to display a list of all users...
def users_list(request):
    userslist = UserInfo.objects.all()
    usernames=[]
    for users in userslist:
        usernames.append(users.username)
    return render(request, 'api/users_list.html', {'users': usernames})
