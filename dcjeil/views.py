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
import string, os

def test(request):
    return render(request, 'test/vue_test.html')

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
