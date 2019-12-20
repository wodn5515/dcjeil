import logging
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
from .models import Post,FixedView
import string, os

# Create your views here.

def board(request, pk):
    pic_list = ['404','405','408']
    view = ['101','102','103','104','105','106','207','501','502','503','504','505','506','507','508','509','510','511','701']
    if pk in view:
        content = 'fixedview.html'
        div = FixedView.objects.get(div=pk)
        return render(request, 'base_board.html', {
            'sidenav' : 'side_nav/side_nav_' + pk[0] + '.html',
            'content' : content,
            'menu_nav' : pk[0],
            'menu_no' : pk[1:],
            'div' : div,
            'title' : div.get_div_display()
            })
    else:
        page = request.GET.get('page','1')
        page_number_range = 8
        if pk in pic_list:
            content = 'piclist.html'
            post_list_all = Post.objects.filter(div=pk).filter(published=1).order_by('-upload_date')
            paginator = Paginator(post_list_all, 12)
        else:
            content = 'list.html'
            post_list_all = Post.objects.filter(div=pk).filter(published=1).order_by('-upload_date')
            paginator = Paginator(post_list_all, 15)
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        start_index = page_number_range * ((int(page)-1)//page_number_range) + 1
        end_index = start_index + page_number_range
        max_index = len(paginator.page_range)+1
        if end_index >= max_index:
            end_index = max_index
        page_range = range(start_index, end_index)
        return render(request, 'base_board.html', {
            'sidenav' : 'side_nav/side_nav_' + pk[0] + '.html',
            'content' : content,
            'menu_nav' : pk[0],
            'menu_no' : pk[1:],
            'post_list' : post_list,
            'page_range' : page_range,
            'total': post_list_all.count()+1,
            'title' : Post.objects.filter(div=pk).first().get_div_display()
        })

def detail(request, menu, pk):
    return render(request, 'base_detail.html', {
        'sidenav' : 'side_nav/side_nav_' + menu[0] + '.html',
        'content' : 'detail.html',
        'menu_nav' : menu[0],
        'menu_no' : menu[1:],
        'post' : Post.objects.get(pk=pk)
    })