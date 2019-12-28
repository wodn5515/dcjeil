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
from .forms import FinduidForm, FindPasswordForm, RegisterForm1, RegisterForm2
import string, os

def not_logged_in(user):
    return not user.is_authenticated

def home(request):
    notice = Post.objects.filter(div='401').filter(published=True).order_by('-upload_date')[:8]
    news_church = Post.objects.filter(div='402').filter(published=True).order_by('-upload_date')[:8]
    news_mate = Post.objects.filter(div='403').filter(published=True).order_by('-upload_date')[:8]
    prayrequest = Post.objects.filter(div='407').filter(published=True).order_by('-upload_date')[:8]
    weekly = Post.objects.filter(div='803').filter(published=True).order_by('-upload_date')[:8]
    photo = Post.objects.filter(div='405').filter(published=True).order_by('-upload_date')[:5]
    return render(request, 'home.html', {
        'notice' : notice,
        'news_church' : news_church,
        'news_mate' : news_mate,
        'prayrequest' : prayrequest,
        'weekly' : weekly,
        'photo' : photo
        })

def finduid(request):
    if request.method == "POST":
        forms = FinduidForm(request.POST)
        if forms.is_valid():
            return redirect(reverse('finduid2'))
    else:
        forms = FinduidForm()
    return render(request, 'registration/finduid.html', {
        'forms' : forms,
        })

def finduid2(request):
    return render(request, 'registration/finduid2.html')

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

@user_passes_test(not_logged_in, 'home')
def register(request):
    if request.method == "POST":
        if request.POST.get("agree", "") == "agree":
            return redirect(reverse('registerform'))
    return render(request, 'registration/register.html')

@user_passes_test(not_logged_in, 'home')
def registerform(request):
    form1 = RegisterForm1()
    form2 = RegisterForm2()
    return render(request, 'registration/registerform.html', {
        'form1' : form1,
        'form2' : form2
    })