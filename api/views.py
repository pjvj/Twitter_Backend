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
from .models import Relationship
from .serializers import UserInfoSerializer
from .forms import UserRegistrationForm
#from django.views.decorators.clickjacking import xframe_options_exempt
from django.template import context

# Create your views here.

def index(request):
    return render(request, 'api/base.html')
    

#Registering the new users, saving the information in the database.
def twitter_register(request):
    #messages="fill"
    if request.method == 'POST':
        username = request.POST.get('username')
        #username is checked for UNIQUE constraint
        if(UserInfo.objects.filter(username=username).exists()): #An error msg is generated 
            messages.error(request, 'Username already exists') #if it already exists.
            f = UserRegistrationForm()                          #And a fresh registration form is created
        else:
            f = UserRegistrationForm(request.POST)
            if f.is_valid():
                f.save()                                                #It is saved in the database otherwise
                messages.success(request, 'Account created successfully') #and a success msg is generated
                f = UserRegistrationForm()                   #A new form is created and rendered for further registration
    else:
        f = UserRegistrationForm()

    #rendering to the register page again.
    return render(request, 'api/register.html', {'form': f })

#Logining the users
def twitter_login(request):
    #check if the session already exists
    if request.session.has_key('logged_in'):
       username = request.session['logged_in']
       contact = UserInfo.objects.get(username=username)    #render to the homepage of the respected user whose
       return render(request, 'api/homepage.html',{'user':contact}) #session was previously saved

    #fresh login if no session exists in cookies storage  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        contact = UserInfo.objects.get(username=username,password=password)
        if contact:                                             #if username ans password exists
            request.session['logged_in'] = username             #save username as session
            return render(request, 'api/homepage.html',{'user':contact})   #and redirect to its homepage
        else:
            messages.error(request, 'Error wrong username/password') #if credentials doesn't match
            form = AuthenticationForm()                             #creates fresh login form
        
    else:
        form = AuthenticationForm()                
    #Rendering the login form in case of errors
    return render(request, 'api/login.html',{'form':form})

#redirecting users to their home pages after login
def twitter_home(request):
    #check if the session already exists
    if request.session.has_key('logged_in'):
       username = request.session['logged_in']
       contact = UserInfo.objects.get(username=username)            
       print("again",username)                     
       #render to the homepage of the respected user whose session was previously saved
       return render(request, 'api/homepage.html',{'user':contact})

    else:
        form = AuthenticationForm()              #A fresh login form is created and rendered on the login page
        return render(request, 'api/login.html',{'form':form})
    #render to the homepage of the respected user who just logged in
    return render(request, 'api/homepage.html',{'user':contact})

#logout the user from the account
def twitter_logout(request):
    try:
        #deleting the session of the user who logouts
        request.session.flush()
        #del request.session['logged_in']
        messages.success(request, 'Account logged out successfully')
    except KeyError:
        messages.error(request, 'No account to log out.')
    form = AuthenticationForm()
    #return render(request, 'api/login.html',{'form':form})
    return render(request, 'api/logout.html')


def delete_post(request):
     username = request.session['logged_in']


def create_post(request):
    username = request.session['logged_in']
    contact = UserInfo.objects.get(username=username)
    

# view function to display a list of all users...
def users_list(request):
    userslist = UserInfo.objects.all()
    usernames=[]
    #currentuser=request.session['logged_in']
    cuser=request.session['logged_in']
    currentuser=UserInfo.objects.get(username=cuser)
    followings=None
    try:
        followings = Relationship.objects.filter(from_person=currentuser)
    except Exception as e:
        pass
    #followings = Relationship.objects.filter(from_person=currentuser)
    following=[]
    if followings:
        for f in followings:
            following.append(f.to_person)  
    for users in userslist:
        if users.username!=currentuser.username:
            usernames.append(users)
    return render(request, 'api/users_list.html', {'users': usernames ,'currentuser':cuser , 'following':following})


def update_followers(request, username, fid):
    #if request.user.is_authenticated():
    cuser=request.session['logged_in']
    currentuser=UserInfo.objects.get(username=cuser)
    user = UserInfo.objects.get(username=username)
    print(username)
    print(fid)
    if fid!=1 :
        if Relationship.objects.filter(from_person=currentuser,to_person=user):
            print("already following")
        else:
            print("chala save")
            Relationship.objects.create(from_person=currentuser,to_person=user)
    else:
        if Relationship.objects.filter(from_person=currentuser,to_person=user):
            print("chala del")
            Relationship.objects.filter(from_person=currentuser,to_person=user).delete()
        else:
            print("You dont follow him/her")
    userslist = UserInfo.objects.all()
    usernames=[]
    followings=None
    try:
        followings = Relationship.objects.filter(from_person=currentuser)
    except Exception as e:
        pass
    #followings = Relationship.objects.filter(from_person=currentuser)
    following=[]
    if followings:
        #print("aaya hu m followings m")
        for f in followings:
            print(f.from_person.username)
            print(f.to_person.username)
            following.append(f.to_person)  
        userslist.remove(currentuser)
        for users in userslist:
            print(users.username)
    '''
    for users in userslist:
        if currentuser.username!=users.username:
            print(users.username)
            usernames.append(users)
    '''
    return render(request,'api/users_list.html',{'users': userslist ,'currentuser':currentuser.username , 'following':following})
    
