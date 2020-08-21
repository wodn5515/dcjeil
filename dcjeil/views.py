import logging
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password
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
from board.models import Post
from data.models import Carousel, Mainmenu
from .forms import UserCheckForm, UpdateForm, SocialUpdateForm
import string, os

# 홈화면
def home(request):
    carousel_list = Carousel.objects.all().order_by('order')
    menu = Mainmenu.objects.all().order_by('order')
    try:
        tab1 = Post.objects.filter(div='201').order_by('-upload_date')[0]
    except:
        tab1 = None
    try:
        tab2 = Post.objects.filter(div__startswith='30').order_by('-upload_date')[0]
    except:
        tab2 = None
    try:
        tab3 = Post.objects.filter(div='205').order_by('-upload_date')[0]
    except:
        tab3 = None
    recent = Post.objects.order_by('-upload_date')[:8]
    main1 = Post.objects.filter(div='401').order_by('-upload_date')[:8]
    main2 = Post.objects.filter(div='402').order_by('-upload_date')[:8]
    main3 = Post.objects.filter(div='403').order_by('-upload_date')[:8]
    main5 = Post.objects.filter(div='407').order_by('-upload_date')[:8]
    main6 = Post.objects.filter(div__startswith='6').order_by('-upload_date')[:8]
    photo = Post.objects.filter(div='405').order_by('-upload_date')[:5]
    return render(request, 'home.html', {
        'carousel_list' : carousel_list,
        'tab1' : tab1,
        'tab2' : tab2,
        'tab3' : tab3,
        'recent' : recent,
        'main1' : main1,
        'main2' : main2,
        'main3' : main3,
        'main5' : main5,
        'main6' : main6,
        'photo' : photo,
        'menu' : menu
        })

# 정보수정 비밀번호 확인
@login_required
def usercheck(request):
    menu = Mainmenu.objects.all().order_by('order')
    form = UserCheckForm(request.POST or None)
    if request.method == 'POST':
        check_pw = request.POST.get('check_pw')
        current_pw = request.user.password
        if check_password(check_pw, current_pw):
            request.session['usercheck'] = True
            return redirect(reverse('userupdate'))
        error = '비밀번호가 일치하지않습니다.'
        return render(request, 'registration/user/usercheck.html', {
            'form':form,
            'error':error,
            'menu': menu
            })
    else:
        if request.user.is_social:
            request.session['usercheck'] = True
            return redirect(reverse('userupdate'))
        request.session['usercheck'] = False
        request.session['userupdate'] = False
        return render(request, 'registration/user/usercheck.html', {
            'form':form,
            'menu': menu
        })

# 정보수정 변경
@login_required
def userupdate(request):
    menu = Mainmenu.objects.all().order_by('order')
    user = request.user
    social_check = user.is_social
    if request.method == "POST":
        if social_check:
            forms = SocialUpdateForm(request.POST, instance=user)
            render_html = 'registration/user/userupdate_social.html'
        else:
            forms = UpdateForm(request.POST, instance=user)
            render_html = 'registration/user/userupdate.html'
        if forms.is_valid():
            forms.save()
            request.session['userupdate'] = True
            return redirect(reverse('userresult'))
        return render(request, render_html, {
            'forms' : forms,
            'menu': menu
        })
    else:
        if not request.session.get('usercheck', False):
            return redirect(reverse('usercheck'))
        request.session['user_check'] = False
        if social_check:
            forms = SocialUpdateForm(instance=user)
            render_html = 'registration/user/userupdate_social.html'
        else:
            forms = UpdateForm(instance=user)
            render_html = 'registration/user/userupdate.html'
        return render(request, render_html, {
            'forms' : forms,
            'menu': menu
        })

# 정보수정 결과
def userresult(request):
    menu = Mainmenu.objects.all().order_by('order')
    if not request.session.get('userupdate', False):
        return redirect(reverse('usercheck'))
    request.session['userupdate'] = False
    return render(request, 'registration/user/userresult.html', {
        'menu': menu
    })