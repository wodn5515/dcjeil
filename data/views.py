import logging
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core import serializers
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.utils.dateparse import parse_date
from django.db import IntegrityError
from el_pagination.views import AjaxListView
from imagekit.utils import get_cache
from random import choice
from .models import History, Server, Pastol, Worship, Community, Welcome, Vision, Nurture, Wayto
import string, os, json

# Create your views here.

def history(request):
    decade = 1970
    data = []
    for i in range(5):
        history_list = History.objects.filter(date__year__gte=decade, date__year__lt=decade+10).order_by('date')
        year_temp = 0
        data_temp = []
        for j in history_list:
            history = {}
            if year_temp != j.date.year:
                year_temp = j.date.year
                history['year'] = str(j.date.year)
            else:
                history['year'] = ' '
            history['date'] = str(j.date.month) + ' / ' + str(j.date.day)
            history['content'] = j.content.replace('\n','<br>')
            data_temp.append(history)
        data.append(data_temp)
        decade += 10
    return JsonResponse(data, safe=False)

def server(request):
    data = {}
    server = Server.objects.get()
    data['content'] = server.content
    return JsonResponse(data, safe=False)

def pastol(request):
    data = {}
    pastol = Pastol.objects.get()
    data['content'] = pastol.content
    return JsonResponse(data, safe=False)

def vision(request):
    data = {}
    vision = Vision.objects.get()
    data['content'] = vision.content
    return JsonResponse(data, safe=False)

def nurture(request):
    data = {}
    nurture = Nurture.objects.get()
    data['content'] = nurture.content
    return JsonResponse(data, safe=False)

def wayto(request):
    data = {}
    wayto = Wayto.objects.get()
    data['content'] = wayto.content
    return JsonResponse(data, safe=False)

def worship(request):
    data = {}
    worship = Worship.objects.get()
    data['content'] = worship.content
    return JsonResponse(data, safe=False)

def community(request, div):
    data = {}
    community = Community.objects.get(div=div)
    data['image'] = community.image.url
    data['title'] = community.title.replace('\n', '<br>')
    data['goal'] = community.goal
    data['worship'] = community.worship.replace('\n', '<br>')
    data['server'] = community.server
    data['youtube'] = community.youtube
    return JsonResponse(data, safe=False)

def welcome(request):
    data = {}
    welcome = Welcome.objects.get()
    data['content'] = welcome.content
    return JsonResponse(data, safe=False)