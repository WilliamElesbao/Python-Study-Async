from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        print(username)
        print(password)
        print(confirm_password)

        if  password == '':
            messages.add_message(request, constants.ERROR, "The password field cannot be null or empty")
            return redirect('/users/register')
        
        if not password == confirm_password:
            messages.add_message(request, constants.ERROR, "Passwords don't match")
            return redirect('/users/register')
        
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.add_message(request, constants.ERROR, "User already exists")
            return redirect('/users/register')
        
        try:
            User.objects.create_user(
                username=username,
                password=password
            )
            return redirect('/users/login') ###
        except:
            messages.add_message(request, constants.ERROR, "Internal server error")
            return redirect('/users/register')

def login(request):
    if request.method == "GET":
        print(request.user)
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # a esquerda coluna do banco e a direita nossa var
        user = auth.authenticate(request, username = username, password =  password)

        if user:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Logged')
            return redirect('/flashcard/new_flashcard/') ###
        else:
            messages.add_message(request, constants.ERROR, 'Username or Passoword is invalid!')
            return redirect('/users/login')

def logout(request):
    auth.logout(request)
    return redirect('/users/login')
