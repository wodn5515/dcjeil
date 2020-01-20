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
from .models import History, Server
from .choice import DIV_CHOICES
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
    for i,j in DIV_CHOICES:
        server_div = []
        server_list = Server.objects.filter(div=i)
        if not server_list:
            continue
        for server in server_list:
            server_temp = {}
            server_temp['name'] = server.name
            server_temp['email'] = server.email
            server_temp['tp'] = server.tp
            server_temp['htp'] = server.htp
            server_temp['office'] = server.get_office_display()
            server_temp['image'] = server.image.url
            server_temp['charge'] = server.charge
            server_div.append(server_temp)
        data[j] = server_div
    return JsonResponse(data, safe=False)