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
from .forms import UserCheckForm, UpdateForm1, UpdateForm2
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
    form = UserCheckForm(request.POST or None)
    if request.method == 'POST':
        check_pw = request.POST.get('check_pw')
        current_pw = request.user.password
        if check_password(check_pw, current_pw):
            request.session['usercheck'] = True
            return redirect(reverse('userupdate'))
        error = '비밀번호가 일치하지않습니다.'
        return render(request, 'user/usercheck.html', {
            'form':form,
            'error':error
            })
    else:
        request.session['usercheck'] = False
        request.session['userupdate'] = False
        return render(request, 'user/usercheck.html', {'form':form})

# 정보수정 변경
@login_required
def userupdate(request):
    if request.method == "POST":
        user = request.user
        forms1 = UpdateForm1(request.POST, instance=user)
        forms2 = UpdateForm2(request.POST, instance=user)
        if forms1.is_valid() and forms2.is_valid():
            forms1.save()
            forms2.save()
            request.session['userupdate'] = True
            return redirect(reverse('userresult'))
        return render(request, 'user/userupdate.html', {
            'forms1' : forms1,
            'forms2' : forms2
        })
    else:
        if not request.session.get('usercheck', False):
            return redirect(reverse('usercheck'))
        user = request.user
        forms1 = UpdateForm1(instance=user)
        forms2 = UpdateForm2(instance=user)
        request.session['user_check'] = False
        return render(request, 'user/userupdate.html', {
            'forms1' : forms1,
            'forms2' : forms2
        })

# 정보수정 결과
def userresult(request):
    if not request.session.get('userupdate', False):
        return redirect(reverse('usercheck'))
    request.session['userupdate'] = False
    return render(request, 'user/userresult.html')