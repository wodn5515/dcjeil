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
from django.views.generic import ListView, DetailView, TemplateView
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.db import IntegrityError
from django.db.models import Q, Count
from el_pagination.views import AjaxListView
from imagekit.utils import get_cache
from random import choice
from menu.models import Mainmenu, Submenu, FixedMenu
from data.models import History, Community
from .utils import BoardMixin, get_menu
from .models import Post, Comment, PostFile
from .forms import AddCommentForm, PostWriteForm, PostSuperuserForm, PostFileFormset
import string, os, json, re, datetime

# Create your views here.

# 게시판 - 목록
class Board(ListView, BoardMixin):

    model = Post
    template_name = "base_board.html"
    paginate_by = 10
    context_object_name = "post_list"

    def get_context_data(self, now_menu, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        kind = self.request.GET.get("s_kind", "")
        keyword = self.request.GET.get("s_keyword", "")
        paginator = context["paginator"]
        page = self.request.GET.get("page", "1")
        now_main = now_menu.mainmenu
        notice_list = (
            Post.objects.filter(div=now_menu)
            .filter(notice=True)
            .order_by("-reservation")
        ).select_related("writer").annotate(comments=Count("comment")).only("writer__is_superuser", "writer__name", "title", "views")
        if now_menu.m_type == "fixed_uneditable":
            if now_menu.name == "교회연혁":
                html = "fixedboard/history.html"
                context["history_decade"], context["fixed_data"] = self.get_history()
            else:
                html = "fixedboard/community.html"
                context["fixed_data"] = self.get_community(pk)
        else:
            if now_menu.m_type == "fixed":
                context["fixed_data"] = FixedMenu.objects.filter(menu=now_menu).last()
            html = now_menu.m_type + ".html"
        context["notice_list"] = notice_list
        context["page_range"] = self.page_range(paginator, page)
        context["pk"] = pk
        context["menu"] = get_menu()
        context["s_kind"] = kind
        context["s_keyword"] = keyword
        context["now_menu"] = now_menu
        context["now_main"] = now_main
        context["html"] = html
        return context

    def get_queryset(self, now_menu):
        kind = self.request.GET.get("s_kind", "")
        keyword = self.request.GET.get("s_keyword", "")
        if self.request.user.is_staff:
            post_list = Post.objects.filter(
                div=now_menu
            ).select_related("writer")
        else:
            post_list = Post.objects.filter(
                Q(div=now_menu), Q(reservation__lte=datetime.datetime.now())
            ).select_related("writer")
        if kind == "title":
            post_list = post_list.filter(
                Q(title__contains=keyword) | Q(date__contains=keyword)
            )
        elif kind == "content":
            post_list = post_list.filter(content__contains=keyword)
        elif kind == "title_content":
            post_list = post_list.filter(
                Q(title__contains=keyword)
                | Q(content__contains=keyword)
                | Q(date__contains=keyword)
            )
        elif kind == "writer":
            post_list = post_list.filter(writer__name__contains=keyword)
        return post_list.order_by("-reservation").select_related("tag").annotate(comments=Count("comment"), files=Count("file"))

    def get(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        try:
            now_menu = Submenu.objects.get(pk=pk)
        except Submenu.DoesNotExist:
            raise Http404("게시판이 존재하지 않습니다.")
        if now_menu.mainmenu.hide:
            if not request.user.is_authenticated:
                messages.info(request, "로그인 후 이용해주세요.")
                return redirect("/login/?next=/")
            else:
                if not request.user.is_media:
                    messages.info(request, "권한이 없습니다.")
                    return redirect("/")
        self.object_list = self.get_queryset(now_menu)
        context = self.get_context_data(now_menu)
        return self.render_to_response(context)


# 게시판 - 디테일
def detail(request, pk):
    try:
        post = Post.objects.select_related("writer").get(pk=pk)
    except Post.DoesNotExist:
        raise Http404("게시글이 존재하지 않습니다.")
    menu = get_menu()
    now_menu = post.div
    try:
        prev_post = Post.objects.filter(
            div=now_menu, reservation__lt=post.reservation
        ).order_by("-reservation").only("title", "reservation")[0]
    except:
        prev_post = None
    try:
        next_post = Post.objects.filter(
            div=now_menu, reservation__gt=post.reservation
        ).order_by("reservation").only("title", "reservation")[0]
    except:
        next_post = None
    return render(
        request,
        "base_detail.html",
        {
            "content": "detail.html",
            "now_main" : now_menu.mainmenu,
            "post": post,
            "board_pk": now_menu.id,
            "pk": pk,
            "prev_post": prev_post,
            "next_post": next_post,
            "menu": menu,
            "now_menu": now_menu,
        },
    )


# 댓글 등록 및 불러오기
def comments(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            data = json.loads(request.body.decode("utf-8"))
            content = data["content"]
            if content == "":
                return HttpResponse("false||0||내용을 입력해주세요.")
            new_comment = Comment(
                post=Post.objects.get(pk=pk), writer=request.user, content=content
            )
            new_comment.save()
            return HttpResponse("true||등록완료")
        else:
            return HttpResponse("false||redirect||로그인 후 이용해주세요.||/login/?next=/")
    else:
        comments = Comment.objects.filter(post=pk).order_by("-date")
        comments_list = []
        for i in comments:
            comment = {}
            comment["id"] = i.id
            comment["content"] = i.content
            comment["date"] = i.date
            comment["name"] = "관리자" if i.writer.is_superuser else i.writer.name
            comments_list.append(comment)
        return JsonResponse(comments_list, safe=False)


# 댓글 삭제
def comment_delete(request, pk):
    if request.method == "POST":
        comment = Comment.objects.get(pk=pk)
        if comment.writer == request.user or request.user.is_superuser:
            comment.delete()
            return HttpResponse("삭제했습니다.")
        return HttpResponse("false||권한이 없습니다.")


# 게시글 작성
def post_write(request, board_pk):
    user = request.user
    if not user.is_authenticated:
        messages.info(request, "로그인 후 이용해주세요.")
        return redirect("/login?next=" + request.path)
    menu = get_menu()
    now_menu = Submenu.objects.get(pk=board_pk)
    permission_menus = []
    for permissions_group in user.boardpermissiongroups.all():
        for permission in permissions_group.permissions.all():
            permission_menus.append(permission.get_full_menu())
    if request.method == "POST":
        if board_pk in permission_menus or user.is_superuser:
            forms = PostSuperuserForm(request.POST)
            fileforms = PostFileFormset(request.POST, request.FILES)
            if forms.is_valid() and fileforms.is_valid():
                reg = re.compile("/upload_files\S*[jpg,png,gif]")
                new_post = forms.save(commit=False)
                new_post.div = now_menu
                new_post.writer = request.user
                try:
                    new_post.image = reg.search(new_post.content).group()
                except:
                    new_post.image = ""
                new_post.save()
                files = fileforms.save(commit=False)
                for file in files:
                    file.post = new_post
                    file.save()
                return redirect(new_post)
            context = {
                "board_pk": board_pk,
                "forms": forms,
                "fileforms": fileforms,
                "menu": menu,
                "now_menu": now_menu,
            }
        else:
            if now_menu.is_allowed_to_all:
                forms = PostWriteForm(request.POST)
            else:
                messages.info(request, "권한이 없습니다.")
                return redirect("board:board", board_pk)
            if forms.is_valid():
                reg = re.compile("/upload_files\S*[jpg,png,gif]")
                new_post = forms.save(commit=False)
                new_post.div = Submenu.objects.filter(mainmenu=int(board_pk[0])).get(
                    order=int(board_pk[1:])
                )
                new_post.writer = request.user
                try:
                    new_post.image = reg.search(new_post.content).group()
                except:
                    new_post.image = ""
                new_post.save()
                return redirect(new_post)
            context = {
                "board_pk": board_pk,
                "forms": forms,
                "menu": menu,
                "now_menu": now_menu,
            }
        return render(request, "board_write.html", context)
    else:
        if board_pk in permission_menus or user.is_superuser:
            forms = PostSuperuserForm()
            fileforms = PostFileFormset(queryset=PostFile.objects.none())
            context = {
                "board_pk": board_pk,
                "forms": forms,
                "fileforms": fileforms,
                "menu": menu,
                "now_menu": now_menu,
            }
        else:
            if now_menu.is_allowed_to_all:
                forms = PostWriteForm()
                context = {
                    "board_pk": board_pk,
                    "forms": forms,
                    "menu": menu,
                    "now_menu": now_menu,
                }
            else:
                messages.info(request, "권한이 없습니다.")
                return redirect("board:board", board_pk)
        return render(request, "board_write.html", context)


# 게시글 수정
def post_update(request, pk):
    user = request.user
    post = Post.objects.get(pk=pk)
    if not user.is_authenticated:
        messages.info(request, "로그인 후 이용해주세요.")
        return redirect(post)
    menu = get_menu()
    files = PostFile.objects.filter(post=post)
    now_menu = post.div
    permission_menus = []
    if post.writer == user:
        if request.method == "POST":
            if user.is_superuser:
                forms = PostSuperuserForm(request.POST, instance=post)
                fileforms = PostFileFormset(request.POST, request.FILES)
                if forms.is_valid() and fileforms.is_valid():
                    reg = re.compile("/upload_files\S*[jpg,png,gif]")
                    updated_post = forms.save(commit=False)
                    updated_post.updated_date = timezone.now()
                    try:
                        updated_post.image = reg.search(updated_post.content).group()
                    except:
                        updated_post.image = ""
                    updated_post.save()
                    files = fileforms.save(commit=False)
                    for file in files:
                        file.post = updated_post
                        file.save()
                    files = fileforms.save()
                    return redirect(updated_post)
                    fileforms = PostFileFormset(queryset=files)
                return render(
                    request,
                    "board_write.html",
                    {
                        "forms": forms,
                        "fileforms": fileforms,
                        "menu": menu,
                        "now_menu": now_menu,
                    },
                )
            else:
                forms = PostWriteForm(request.POST, instance=post)
                if forms.is_valid():
                    reg = re.compile("/upload_files\S*[jpg,png,gif]")
                    updated_post = forms.save(commit=False)
                    try:
                        updated_post.image = reg.search(updated_post.content).group()
                    except:
                        updated_post.image = ""
                    updated_post.save()
                    return redirect(updated_post)
                return render(
                    request,
                    "board_write.html",
                    {
                        "forms": forms,
                        "menu": menu,
                        "now_menu": now_menu,
                    },
                )
        else:
            if user.is_superuser:
                forms = PostSuperuserForm(instance=post)
                fileforms = PostFileFormset(queryset=files)
                return render(
                    request,
                    "board_write.html",
                    {
                        "forms": forms,
                        "fileforms": fileforms,
                        "menu": menu,
                        "now_menu": now_menu,
                    },
                )
            else:
                forms = PostWriteForm(instance=post)
                return render(
                    request,
                    "board_write.html",
                    {
                        "forms": forms,
                        "menu": menu,
                        "now_menu": now_menu,
                    },
                )
    else:
        messages.info(request, "권한이 없습니다.")
        return redirect(post)


# 게시글 삭제
def post_delete(request, menu, pk):
    post = Post.objects.get(pk=pk)
    user = request.user
    if post.writer == user or user.is_superuser:
        post.delete()
        return redirect("board:board", menu)
    else:
        messages.info(request, "권한이 없습니다.")
        return redirect(post)


###############################################################################################
########################################## Abandoned ##########################################
###############################################################################################
###############################################################################################
########################################## Abandoned ##########################################
###############################################################################################
###############################################################################################
########################################## Abandoned ##########################################
###############################################################################################
###############################################################################################
########################################## Abandoned ##########################################
###############################################################################################
###############################################################################################
########################################## Abandoned ##########################################
###############################################################################################
"""
# 게시판 목록
def board(request, pk):
    kind = request.GET.get('s_kind', '')
    keyword = request.GET.get('s_keyword', '')
    menu = Mainmenu.objects.all().order_by('order')
    menu_nav = pk[0]
    menu_no = pk[1:]
    now_menu = Submenu.objects.filter(mainmenu=menu_nav).get(order=int(menu_no))
    notice_list = Post.objects.filter(div=pk).filter(notice=True).order_by('-upload_date')
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
    if now_menu.m_type == 'fixed_uneditable':
        content = 'fixedboard/fixedboard_' + pk + '.html'
    else:
        content = now_menu.m_type + '.html'
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
"""

###############################################################################################
########################################## Abandoned ##########################################
###############################################################################################
###############################################################################################
########################################## Abandoned ##########################################
###############################################################################################
###############################################################################################
########################################## Abandoned ##########################################
###############################################################################################
###############################################################################################
########################################## Abandoned ##########################################
###############################################################################################
###############################################################################################
########################################## Abandoned ##########################################
###############################################################################################
