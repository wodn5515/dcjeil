import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.views.generic import ListView, DetailView
from django.utils.dateparse import parse_date
from django.db import IntegrityError
from el_pagination.views import AjaxListView
from imagekit.utils import get_cache
from random import choice
from .models import User
from board.models import Post
from .forms import FinduidForm, FindPasswordForm, RegisterForm1, RegisterForm2, LoginForm
import string, os

# Create your views here.

def not_logged_in(user):
    return not user.is_authenticated

######################################################

# 로그인 화면
def login_view(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return HttpResponseRedirect(request.GET.get('next'))
    return render(request, 'registration/login.html', {'form': form })

# 아이디 찾기 입력창
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

# 아이디 찾기 결과창
def finduid2(request):
    return render(request, 'registration/finduid2.html')

# 비밀번호 찾기 입력창
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

# 비밀번호 찾기 결과창
def findpassword2(request):
    return render(request, 'registration/findpassword2.html')

# 회원가입 약관
@user_passes_test(not_logged_in, 'home')
def register(request):
    if request.method == "POST":
        if request.POST.get("term_agree", "") == "agree" and request.POST.get("private_agree","") == "agree":
            request.session['register_agree'] = True
            return redirect(reverse('registerform'))
        messages.info(request,"회원가입약관 및 개인정보처리방침안내의 내용에 동의하셔야 회원가입을 하실 수 있습니다.")
        return render(request, 'registration/register.html')
    else:
        request.session['register_agree'] = False
        request.session['register_submit'] = False
        return render(request, 'registration/register.html')

# 회원가입 입력창
@user_passes_test(not_logged_in, 'home')
def registerform(request):
    if request.method == "POST":
        forms1 = RegisterForm1(request.POST)
        forms2 = RegisterForm2(request.POST)
        if forms1.is_valid() and forms2.is_valid():
            temp_new_account = forms1.save(commit=False)
            new_account = RegisterForm2(request.POST, instance=temp_new_account)
            new_account.save()
            request.session['register_submit'] = True
            return redirect(reverse('registersubmit'))
        return render(request, 'registration/registerform.html', {
            'forms1' : forms1,
            'forms2' : forms2
        })
    else:
        if not request.session.get('register_agree', False):
            return redirect(reverse('register'))
        forms1 = RegisterForm1()
        forms2 = RegisterForm2()
        request.session['register_agree'] = False
        return render(request, 'registration/registerform.html', {
            'forms1' : forms1,
            'forms2' : forms2
        })

# 회원가입 결과창
@user_passes_test(not_logged_in, 'home')
def registersubmit(request):
    if not request.session.get('register_submit', False):
        return redirect(reverse('register'))
    request.session['register_submit'] = False
    return render(request, 'registration/registerresult.html')