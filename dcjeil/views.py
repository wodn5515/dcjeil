import logging
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.db import IntegrityError
from django.db.models import Q
from el_pagination.views import AjaxListView
from imagekit.utils import get_cache
from random import choice
from board.models import Post
from data.models import Carousel, Popup
from menu.models import Mainmenu, Submenu
from .forms import UserCheckForm, UpdateForm, SocialUpdateForm
from board.utils import get_menu
import string, os, datetime

# 홈화면
def home(request):
    carousel_list = Carousel.objects.all().order_by("order")
    menu = get_menu()
    try:
        tab1 = Post.objects.filter(Q(div__mainmenu__order=2), Q(reservation__lte=datetime.datetime.now())).select_related("div").only("div__name", "video", "date", "title", "words").order_by("-reservation").first()
    except:
        tab1 = None
    try:
        tab2 = Post.objects.filter(Q(div__mainmenu__order=3), Q(reservation__lte=datetime.datetime.now())).select_related("div").only("div__name", "date", "title").order_by("-reservation").first()
    except:
        tab2 = None
    main_recent = Post.objects.filter(
        reservation__lte=datetime.datetime.now()
    ).order_by("-reservation")[:8].select_related("div").only("div__mainmenu", "div__mainmenu__order", "div__order", "div__name", "preacher", "tag", "date", "title", "upload_date")
    main_menu_set = Submenu.objects.filter(exposure_home__gt=0).only("name", "order")
    photo_menu = Submenu.objects.filter(name="교회앨범").only("name", "order").first()
    context = {
        "carousel_list": carousel_list,
        "tab1": tab1,
        "tab2": tab2,
        "main_recent": main_recent,
        "main_menu_set": main_menu_set,
        "photo_menu": photo_menu,
        "menu": menu,
    }
    popup_cookies = request.COOKIES.get("popup", False)
    popup_list = Popup.objects.filter(
        Q(start_date__lt=datetime.datetime.now()),
        Q(end_date__gt=datetime.datetime.now()),
    )
    if popup_cookies:
        popup_cookies_list = popup_cookies.split("|")
        popup_list = popup_list.exclude(pk__in=popup_cookies_list)
    context["popup_list"] = popup_list
    return render(request, "home.html", context)


# 정보수정 비밀번호 확인
@login_required
def usercheck(request):
    menu = Mainmenu.objects.all().order_by("order")
    form = UserCheckForm(request.POST or None)
    if request.method == "POST":
        check_pw = request.POST.get("check_pw")
        current_pw = request.user.password
        if check_password(check_pw, current_pw):
            request.session["usercheck"] = True
            return redirect(reverse("userupdate"))
        error = "비밀번호가 일치하지않습니다."
        return render(
            request,
            "registration/user/usercheck.html",
            {"form": form, "error": error, "menu": menu},
        )
    else:
        if request.user.is_social:
            request.session["usercheck"] = True
            return redirect(reverse("userupdate"))
        request.session["usercheck"] = False
        request.session["userupdate"] = False
        return render(
            request, "registration/user/usercheck.html", {"form": form, "menu": menu}
        )


# 정보수정 변경
@login_required
def userupdate(request):
    menu = Mainmenu.objects.all().order_by("order")
    user = request.user
    social_check = user.is_social
    if request.method == "POST":
        if social_check:
            forms = SocialUpdateForm(request.POST, instance=user)
            render_html = "registration/user/userupdate_social.html"
        else:
            forms = UpdateForm(request.POST, instance=user)
            render_html = "registration/user/userupdate.html"
        if forms.is_valid():
            forms.save()
            request.session["userupdate"] = True
            return redirect(reverse("userresult"))
        return render(request, render_html, {"forms": forms, "menu": menu})
    else:
        if not request.session.get("usercheck", False):
            return redirect(reverse("usercheck"))
        request.session["user_check"] = False
        if social_check:
            forms = SocialUpdateForm(instance=user)
            render_html = "registration/user/userupdate_social.html"
        else:
            forms = UpdateForm(instance=user)
            render_html = "registration/user/userupdate.html"
        return render(request, render_html, {"forms": forms, "menu": menu})


# 정보수정 결과
def userresult(request):
    menu = Mainmenu.objects.all().order_by("order")
    if not request.session.get("userupdate", False):
        return redirect(reverse("usercheck"))
    request.session["userupdate"] = False
    return render(request, "registration/user/userresult.html", {"menu": menu})
