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
from .models import User
from board.models import Post
from .forms import FinduidForm, FindPasswordForm, RegisterForm1, RegisterForm2
import string, os

# Create your views here.

def not_logged_in(user):
    return not user.is_authenticated

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
    if request.method == "POST":
        forms1 = RegisterForm1(request.POST)
        forms2 = RegisterForm2(request.POST)
        if forms1.is_valid() and forms2.is_valid():
            temp_new_account = forms1.save(commit=False)
            new_account = RegisterForm2(request.POST, instance=temp_new_account)
            new_account.save()
            return HttpResponse('성공')
    else:
        forms1 = RegisterForm1()
        forms2 = RegisterForm2()
    return render(request, 'registration/registerform.html', {
        'forms1' : forms1,
        'forms2' : forms2
    })