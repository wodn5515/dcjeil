import logging
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.utils.dateparse import parse_date
from django.db import IntegrityError
from el_pagination.views import AjaxListView
from imagekit.utils import get_cache
from random import choice
from account.models import User
from board.models import Post
from .forms import FindUsernameForm, FindPasswordForm, RegisterForm1, RegisterForm2
import string, os

def home(request):
    notice = Post.objects.filter(div='401').filter(published=True).order_by('-upload_date')[:8]
    news_church = Post.objects.filter(div='402').filter(published=True).order_by('-upload_date')[:8]
    news_mate = Post.objects.filter(div='403').filter(published=True).order_by('-upload_date')[:8]
    prayrequest = Post.objects.filter(div='407').filter(published=True).order_by('-upload_date')[:8]
    weekly = Post.objects.filter(div='803').filter(published=True).order_by('-upload_date')[:8]
    return render(request, 'home.html', {
        'notice' : notice,
        'news_church' : news_church,
        'news_mate' : news_mate,
        'prayrequest' : prayrequest,
        'weekly' : weekly
        })

def findusername(request):
    if request.method == "POST":
        forms = FindUsernameForm(request.POST)
        if forms.is_valid():
            return redirect(reverse('findusername2'))
    else:
        forms = FindUsernameForm()
    return render(request, 'registration/findusername.html', {
        'forms' : forms,
        })

def findusername2(request):
    return render(request, 'registration/findusername2.html')

def findpassword(request):
    if request.method == "POST":
        forms = FindPasswordForm(request.POST)
        if forms.is_valid():
            return redirect(reverse('findpassword2'))
    else:
        forms = FindPasswordForm()
    return render(request, 'registration/findpassword.html', {
        'forms' : forms
        })

def findpassword2(request):
    return render(request, 'registration/findpassword2.html')

def register(request):
    if request.method == "POST":
        if request.POST.get("agree", "") == "agree":
            return redirect(reverse('registerform'))
    return render(request, 'registration/register.html')

def registerform(request):
    form1 = RegisterForm1()
    form2 = RegisterForm2()
    return render(request, 'registration/registerform.html', {
        'form1' : form1,
        'form2' : form2
    })