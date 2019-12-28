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

def get_title(pk):
        div_arr = {'101':'인사말', '102':'교회연혁', '103':'우리의 비젼',
        '104':'담임목사소개', '105':'섬기는 사람들', '106':'찾아오시는 길',
        '201':'금주의 말씀', '202':'주일오후예배', '203':'수요예배', '207':'예배안내',
        '204':'금요철야예배', '205':'새벽기도', '206':'부흥회',
        '301':'할렐루야 찬양대', '302':'호산나 찬양대', '303':'찬양, 간증 집회',
        '401':'공지사항', '402':'교회소식', '403':'교우소식', '404':'새가족소개',
        '405':'교회앨범', '406':'자유게시판', '407':'기도요청', '408':'행사동영상', '409':'큐티나눔방',
        '501':'영아부', '502':'유치부', '503':'유년부',
        '504':'초등부', '505':'중등부', '506':'고등부', '507':'사랑부',
        '508':'청년1부', '509':'청년2부', '510':'청년3부', '511':'어린이집',
        '601':'선교위원회','602':'국내선교','603':'캄보디아','604':'인도','605':'일본','606':'태국',
        '607':'필리핀','608':'이집트','609':'탄자니아','610':'카메룬','611':'남아공','612':'러시아',
        '613':'볼리비아','614':'파푸아뉴기니','615':'헝가리','616':'단기선교',
        '701':'양육시스템', '702':'새가족부 자료실', '703':'확신반 자료실',
        '801':'문서자료실', '802':'기타자료실', '803':'주보자료실',
        }
        return div_arr[pk]

def board(request, pk):
    pic_list = ['404','405','408']
    fixedboard = ['101','102','103','104','105','106','207','501','502','503','504','505','506','507','508','509','510','511','701']
    if pk in fixedboard:
        content = 'fixedboard/fixedboard_' + pk + '.html'
        return render(request, 'base_board.html', {
            'sidenav' : 'side_nav/side_nav_' + pk[0] + '.html',
            'content' : content,
            'menu_nav' : pk[0],
            'menu_no' : pk[1:],
            'title' : get_title(pk)
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
            'title' : get_title(pk)
        })

def detail(request, menu, pk):
    return render(request, 'base_detail.html', {
        'sidenav' : 'side_nav/side_nav_' + menu[0] + '.html',
        'content' : 'detail.html',
        'menu_nav' : menu[0],
        'menu_no' : menu[1:],
        'post' : Post.objects.get(pk=pk),
        'title' : get_title(menu)
    })