import logging
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
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
from django.db.models import Q
from el_pagination.views import AjaxListView
from imagekit.utils import get_cache
from random import choice
from data.models import Mainmenu, Submenu
from .models import Post, Comment, PostFile
from .forms import AddCommentForm, PostWriteForm, PostSuperuserForm, PostFileFormset
import string, os, json, re

# Create your views here.

def get_title(pk):
        div_arr = {'101':'인사말', '102':'교회연혁', '103':'우리의 비젼',
        '104':'담임목사소개', '105':'섬기는 사람들', '106':'찾아오시는 길',
        '201':'금주의 말씀', '202':'주일오후예배', '203':'수요예배', '207':'예배안내',
        '204':'금요철야예배', '205':'새벽기도', '206':'부흥회',
        '301':'할렐루야 찬양대', '302':'호산나 찬양대', '303':'찬양, 간증 집회',
        '401':'공지사항', '402':'교회소식', '403':'교우소식', '404':'새가족소개',
        '405':'교회앨범', '406':'자유게시판', '407':'기도요청', '408':'행사동영상', '409':'큐티나눔방',
        '501':'사랑부', '502':'영아부', '503':'유치부',
        '504':'유년부', '505':'초등부', '506':'중등부', '507':'고등부',
        '508':'청년1부', '509':'청년2부', '510':'청년3부',
        '601':'선교위원회','602':'국내선교','603':'아시아','604':'아프리카','605':'기타','606':'단기선교',
        '701':'양육시스템', '702':'새가족부 자료실', '703':'확신반 자료실',
        '801':'문서자료실', '802':'기타자료실', '803':'주보자료실',
        }
        return div_arr[pk]

def board(request, pk):
    kind = request.GET.get('s_kind', '')
    keyword = request.GET.get('s_keyword', '')
    menu = Mainmenu.objects.all().order_by('order')
    menu_nav = pk[0]
    menu_no = pk[1:]
    now_menu = Submenu.objects.filter(mainmenu=menu_nav).get(order=int(menu_no))
    if now_menu.m_type == 'fixed':
        content = 'fixedboard/fixedboard_' + pk + '.html'
    else:
        content = now_menu.m_type + '.html'
    notice_list = Post.objects.filter(div=pk).filter(notice=True)
    page = request.GET.get('page','1')
    page_number_range = 5
    if kind == 'title':
        post_list_all =  Post.objects.filter(div=pk).filter(Q(title__contains=keyword)|Q(date__contains=keyword)).order_by('-upload_date')
    elif kind == 'content':
        post_list_all =  Post.objects.filter(div=pk).filter(content__contains=keyword).order_by('-upload_date')
    elif kind == 'title_content':
        post_list_all =  Post.objects.filter(div=pk).filter(Q(title__contains=keyword)|Q(content__contains=keyword)|Q(date__contains=keyword)).order_by('-upload_date')
    elif kind == 'writer':
        post_list_all =  Post.objects.filter(div=pk).filter(writer__name__contains=keyword).order_by('-upload_date')
    else:
        post_list_all = Post.objects.filter(div=pk).order_by('-upload_date')
    paginator = Paginator(post_list_all, 16)
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
        'content' : content,
        'menu_nav' : menu_nav,
        'menu_no' : menu_no,
        'notice_list' : notice_list,
        'post_list' : post_list,
        'page_range' : page_range,
        'pk' : pk,
        'total': post_list_all.count()+1,
        's_keyword' : keyword,
        's_kind' : kind,
        'menu' : menu,
        'now_menu' : now_menu
    })

def detail(request, borad_pk, pk):
    post = Post.objects.get(pk=pk)
    menu = Mainmenu.objects.all().order_by('order')
    menu_nav = borad_pk[0]
    menu_no = borad_pk[1:]
    now_menu = Submenu.objects.filter(mainmenu=menu_nav).get(order=int(menu_no))
    try:
        prev_post = Post.objects.filter(div=menu, upload_date__lt=post.upload_date).order_by('-upload_date')[0]
    except:
        prev_post = None
    try:
        next_post = Post.objects.filter(div=menu, upload_date__gt=post.upload_date).order_by('upload_date')[0]
    except:
        next_post = None
    return render(request, 'base_detail.html', {
        'content' : 'detail.html',
        'menu_nav' : menu_nav,
        'menu_no' : menu_no,
        'post' : post,
        'board_pk' : borad_pk,
        'pk': pk,
        'prev_post' : prev_post,
        'next_post' : next_post,
        'menu' : menu,
        'now_menu' : now_menu
    })

def comments(request, pk):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body.decode("utf-8"))
            content = data['content']
            if content == '':
                return HttpResponse('false||0||내용을 입력해주세요.')
            new_comment = Comment(
                post=Post.objects.get(pk=pk),
                writer=request.user,
                content=content
            )
            new_comment.save()
            return HttpResponse('true||등록완료')
        else:
            return HttpResponse('false||redirect||로그인 후 이용해주세요.||/login/?next=' + request.path)
    else:
        comments = Comment.objects.filter(post=pk).order_by('-date')
        comments_list = []
        for i in comments:
            comment = {}
            comment['id'] = i.id
            comment['content'] = i.content
            comment['date'] = i.date
            comment['name'] = i.writer.name
            comments_list.append(comment)
        return JsonResponse(comments_list, safe=False)

def comment_delete(request, pk):
    if request.method == "POST":
        comment = Comment.objects.get(pk=pk)
        if comment.writer == request.user or request.user.is_superuser:
            comment.delete()
            return HttpResponse('삭제했습니다.')
        return HttpResponse('false||권한이 없습니다.')

def post_write(request,borad_pk):
    user = request.user
    active = ['406','407','409','601','602','603','604','605','606','607','608','609','610','611','612','613','614','615','616']
    menu = Mainmenu.objects.all().order_by('order')
    menu_nav = borad_pk[0]
    menu_no = borad_pk[1:]
    now_menu = Submenu.objects.filter(mainmenu=menu_nav).get(order=int(menu_no))
    if request.method == "POST":
        if not user.is_authenticated:
            messages.info(request, '로그인 후 이용해주세요.')
            return redirect('/login?next='+request.path)
        if borad_pk not in active:
            if not user.is_superuser:
                messages.info(request, '관리자만 이용가능합니다.')
                return redirect('board:board', borad_pk)
            else:
                forms = PostSuperuserForm(request.POST)
                fileforms = PostFileFormset(request.POST, request.FILES)
                if forms.is_valid() and fileforms.is_valid():
                    reg = re.compile('/upload_files\S*[jpg,png,gif]')
                    new_post = forms.save(commit=False)
                    new_post.div = borad_pk
                    new_post.writer = request.user
                    try:
                        new_post.image = reg.search(new_post.content).group()
                    except:
                        new_post.image = ''
                    new_post.save()
                    files = fileforms.save(commit=False)
                    for file in files:
                        file.post = new_post
                        file.save()
                    return redirect(new_post)
        else:
            forms = PostWriteForm(request.POST)
            if forms.is_valid():
                reg = re.compile('/upload_files\S*[jpg,png,gif]')
                new_post = forms.save(commit=False)
                new_post.div = borad_pk
                new_post.writer = request.user
                try:
                    new_post.image = reg.search(new_post.content).group()
                except:
                    new_post.image = ''
                new_post.save()
                return redirect(new_post)
        return render(request, 'board_write.html', {
            'borad_pk' : borad_pk,
            'forms' : forms,
            'fileforms' : fileforms,
            'menu' : menu,
            'now_menu' : now_menu
        })
    else:
        if not user.is_authenticated:
            messages.info(request, '로그인 후 이용해주세요.')
            return redirect('/login?next='+request.path)
        if menu not in active:
            if not user.is_superuser:
                messages.info(request, '관리자만 이용가능합니다.')
                return redirect('board:board', borad_pk)
            else:
                forms = PostSuperuserForm()
                fileforms = PostFileFormset(queryset=PostFile.objects.none())
            return render(request, 'board_write.html', {
                'borad_pk' : borad_pk,
                'forms' : forms,
                'fileforms' : fileforms,
                'menu' : menu,
                'now_menu' : now_menu
            })
        else:
            forms = PostWriteForm()
        return render(request, 'board_write.html', {
            'borad_pk' : borad_pk,
            'forms' : forms,
            'menu' : menu,
            'now_menu' : now_menu
        })

def post_update(request, borad_pk, pk):
    active = ['406','407','409','601','602','603','604','605','606']
    menu = Mainmenu.objects.all().order_by('order')
    user = request.user
    post = Post.objects.get(pk=pk)
    files = PostFile.objects.filter(post=post)
    if user.is_superuser:
        if request.method == 'POST':
            forms = PostSuperuserForm(request.POST, instance=post)
            fileforms = PostFileFormset(request.POST, request.FILES)
            if forms.is_valid() and fileforms.is_valid():
                reg = re.compile('/upload_files\S*[jpg,png,gif]')
                updated_post = forms.save(commit=False)
                try:
                    updated_post.image = reg.search(updated_post.content).group()
                except:
                    updated_post.image = ''
                updated_post.save()
                files = fileforms.save()
                return redirect(updated_post)
            fileforms = PostFileFormset(queryset=files)
            return render(request, 'board_write.html', {
                'borad_pk' : borad_pk,
                'forms' : forms,
                'fileforms' : fileforms,
                'menu' : menu,
                'now_menu' : now_menu
            }) 
        else:
            forms = PostSuperuserForm(instance=post)
            fileforms = PostFileFormset(queryset=files)
            return render(request, 'board_write.html', {
                'borad_pk' : borad_pk,
                'forms' : forms,
                'fileforms' : fileforms,
                'menu' : menu,
                'now_menu' : now_menu
            })
    elif post.writer == user:
        if request.method == 'POST':
            forms = PostWriteForm(request.POST, instance=post)
            if forms.is_valid():
                reg = re.compile('/upload_files\S*[jpg,png,gif]')
                updated_post = forms.save(commit=False)
                try:
                    updated_post.image = reg.search(updated_post.content).group()
                except:
                    updated_post.image = ''
                updated_post.save()
                return redirect(updated_post)
            return render(request, 'board_write.html', {
                'borad_pk' : borad_pk,
                'forms' : forms,
                'menu' : menu,
                'now_menu' : now_menu
            })
        else:
            forms = PostWriteForm(instance=post)
            return render(request, 'board_write.html', {
                'borad_pk' : borad_pk,
                'forms' : forms,
                'menu' : menu,
                'now_menu' : now_menu
            })
    else:
        messages.info(request, '권한이 없습니다.')
        return redirect(post)

def post_delete(request, menu, pk):
    post = Post.objects.get(pk=pk)
    user = request.user
    if post.writer == user or user.is_superuser:
        post.delete()
        return redirect('board:board', menu)
    else:
        messages.info('권한이 없습니다.')
        return redirect(post)