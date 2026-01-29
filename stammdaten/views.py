from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def start(request):
    return HttpResponse("Startseite")

def user_login(request):
    name = request.POST['name']
    password = request.POST['password']
    cont = request.POST['cont']
    user = authenticate(request, username=name, password=password)
    if user is not None:
        login(request, user)
    if ":" in cont:                     # url auflösen
        count = reverse(count)
    return redirect(cont)
    # Redirect to a success page.

def user_logout(request):
    cont = request.POST['cont']
    logout(request)
    return redirect(cont)