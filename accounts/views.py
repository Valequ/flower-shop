from django.shortcuts import render

# Create your views here.

def profile(requset):
    return render (requset,'accounts/profile.html')
def login(requset):
    return render (requset,'accounts/login.html')
def register(requset):
    return render (requset,'accounts/register.html')