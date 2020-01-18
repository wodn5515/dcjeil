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
from board.models import Post
from data.models import Carousel
import string, os

def test(request):
    return render(request, 'test/vue_test.html')

def home(request):
    carousel_list = Carousel.objects.all().order_by('order')
    tab1 = Post.objects.filter(div='201').order_by('-upload_date')[0]
    tab2 = Post.objects.filter(div__startswith='30').order_by('-upload_date')[0]
    tab3 = Post.objects.filter(div='205').order_by('-upload_date')[0]
    recent = Post.objects.order_by('-upload_date')[:8]
    notice = Post.objects.filter(div='401').order_by('-upload_date')[:8]
    news_church = Post.objects.filter(div='402').order_by('-upload_date')[:8]
    news_mate = Post.objects.filter(div='403').order_by('-upload_date')[:8]
    prayrequest = Post.objects.filter(div='407').order_by('-upload_date')[:8]
    weekly = Post.objects.filter(div='803').order_by('-upload_date')[:8]
    photo = Post.objects.filter(div='405').order_by('-upload_date')[:5]
    return render(request, 'home.html', {
        'carousel_list' : carousel_list,
        'tab1' : tab1,
        'tab2' : tab2,
        'tab3' : tab3,
        'recent' : recent,
        'notice' : notice,
        'news_church' : news_church,
        'news_mate' : news_mate,
        'prayrequest' : prayrequest,
        'weekly' : weekly,
        'photo' : photo
        })
