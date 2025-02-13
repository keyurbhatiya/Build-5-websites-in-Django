from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# @login_required(login_url='login')
def test(request):
    return render(request,'blog/home.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('upassword')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            return redirect('login')
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password is incorrect')
            return redirect('login')
            
    return render(request,'blog/login.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        name = request.POST.get('uname')
        email = request.POST.get('uemail')
        password = request.POST.get('upassword')
        
        try:
            if User.objects.filter(username=name).exists():
                messages.error(request, 'Username already exists')
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered')
                return redirect('signup')
                
            user = User.objects.create_user(username=name, email=email, password=password)
            user.save()
            auth_login(request, user)
            return redirect('home')
        except:
            messages.error(request, 'An error occurred during registration')
            return redirect('signup')
            
    return render(request,'blog/signup.html')

# @login_required(login_url='login')
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request,'blog/home.html', context)

@login_required(login_url='login')
def newPost(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content:
            newPost = models.Post(title=title, content=content, author=request.user)
            newPost.save()
            messages.success(request, 'Post created successfully')
            return redirect('home')
        else:
            messages.error(request, 'Please fill all fields')
            
    return render(request,'blog/newPost.html')

@login_required(login_url='login')
def myPost(request):
    context = {
        'posts': Post.objects.filter(author=request.user)
    }
    return render(request,'blog/myPost.html', context)

@login_required(login_url='login')
def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')






