import logging
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.middleware.csrf import _compare_masked_tokens
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.views.generic import ListView, DetailView, View
from django.utils.dateparse import parse_date
from django.db import IntegrityError
from el_pagination.views import AjaxListView
from imagekit.utils import get_cache
from random import choice
from .models import User
from .forms import FinduidForm, FindPasswordForm, RegisterForm, LoginForm
from .oauth.providers.naver import NaverLoginMixin
from .oauth.providers.kakao import KakaoLoginMixin
from .oauth.providers.google import GoogleLoginMixin
from board.models import Post
from menu.models import Mainmenu
from dcjeil.forms import SocialUpdateForm
import string, os

# Create your views here.

def not_logged_in(user):
    return not user.is_authenticated

def logged_in(user):
    return user.is_authenticated

######################################################

# 로그인 화면
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    menu = Mainmenu.objects.all().order_by('order')
    forms = LoginForm(request.POST or None)
    if request.POST and forms.is_valid():
        user = forms.login(request)
        if user:
            login(request, user)
            return HttpResponseRedirect(request.GET.get('next') if request.GET.get('next') else '/')
    return render(request, 'registration/login.html', {
        'forms': forms,
        'menu': menu
        })

# 아이디 찾기 입력창
def finduid(request):
    if request.method == "POST":
        forms = FinduidForm(request.POST)
        if forms.is_valid():
            return redirect(reverse('finduid2'))
    else:
        forms = FinduidForm()
    return render(request, 'registration/finduid.html', {
        'forms' : forms,
        })

# 아이디 찾기 결과창
def finduid2(request):
    return render(request, 'registration/finduid2.html')

# 비밀번호 찾기 입력창
def findpassword(request):
    if request.method == "POST":
        forms = FindPasswordForm(request.POST)
        if forms.is_valid():
            return redirect(reverse('findpassword2'))
    else:
        forms = FindPasswordForm()
    return render(request, 'registration/findpassword.html', {
        'forms' : forms
        })

# 비밀번호 찾기 결과창
def findpassword2(request):
    return render(request, 'registration/findpassword2.html')

# 회원가입 약관
@user_passes_test(not_logged_in, 'home')
def register(request):
    menu = Mainmenu.objects.all().order_by('order')
    if request.method == "POST":
        if request.POST.get("term_agree", "") == "agree" and request.POST.get("private_agree","") == "agree":
            request.session['register_agree'] = True
            return redirect(reverse('registerform'))
        messages.info(request,"회원가입약관 및 개인정보처리방침안내의 내용에 동의하셔야 회원가입을 하실 수 있습니다.")
        return render(request, 'registration/register.html', {
            'menu': menu
        })
    else:
        request.session['social_login'] = False
        request.session['register_agree'] = False
        request.session['register_submit'] = False
        return render(request, 'registration/register.html', {
            'menu': menu
        })

# 회원가입 입력창
@user_passes_test(not_logged_in, 'home')
def registerform(request):
    menu = Mainmenu.objects.all().order_by('order')
    if request.method == "POST":
        if request.session.get('social_login', False):
            uid = request.session.get('uid')
            user = get_object_or_404(User, uid=uid)
            forms = SocialUpdateForm(request.POST, instance=user)
            if forms.is_valid():
                new_account = forms.save(commit=False)
                new_account.save()
                request.session['register_submit'] = True
                return redirect(reverse('registersubmit'))
            return render(request, 'registration/registerform_social.html', {
                'forms' : forms,
                'menu': menu
            })
        else:
            forms = RegisterForm(request.POST)
            if forms.is_valid():
                new_account = forms.save(commit=False)
                new_account.save()
                request.session['register_submit'] = True
                return redirect(reverse('registersubmit'))
            return render(request, 'registration/registerform.html', {
                'forms' : forms,
                'menu': menu
            })
    else:
        if request.session.get('social_login', False):
            forms = SocialUpdateForm()
            return render(request, 'registration/registerform_social.html', {
                'forms': forms,
                'menu': menu
            })
        else:
            if not request.session.get('register_agree', False):
                return redirect(reverse('register'))
            request.session['register_agree'] = False
            forms = RegisterForm()
            return render(request, 'registration/registerform.html', {
                'forms' : forms,
                'menu': menu
            })

# 회원가입 결과창
@user_passes_test(not_logged_in, 'home')
def registersubmit(request):
    menu = Mainmenu.objects.all().order_by('order')
    if not request.session.get('register_submit', False):
        return redirect(reverse('register'))
    request.session['register_submit'] = False
    return render(request, 'registration/registerresult.html', {
        'menu': menu
    })

# 네이버 소셜 로그인
class NaverLoginCallbackView(NaverLoginMixin, View):
    
    success_url = '/registerform'
    failure_url = settings.LOGIN_URL
    model = get_user_model()

    def get(self, request, *args, **kwargs):
        success_url = request.GET.get('next', '/')
        csrf_token = request.GET.get('state')
        code = request.GET.get('code')
        if not _compare_masked_tokens(csrf_token, request.COOKIES.get('csrftoken')): # state(csrf_token)이 잘못된 경우
            messages.error(request, '잘못된 경로로 로그인하셨습니다.', extra_tags='danger')
            return HttpResponseRedirect(self.failure_url)
        is_success, error = self.login_with_naver(csrf_token, code)
        if not is_success: # 로그인 실패할 경우
            messages.error(request, error, extra_tags='danger')
        if not error.is_active:
            if not error.name:
                self.set_session(register_agree=True, social_login=True)
                return HttpResponseRedirect(self.success_url if is_success else self.failure_url)
            else:
                request.session['register_submit'] = True
                return redirect(reverse('registersubmit'))
        if error.is_active:
            login(request, error, 'member.oauth.backends.SocialLoginBackend') # SocialLoginBackend를 통한 인증 시도
            self.success_url = '/'
            return HttpResponseRedirect(success_url if is_success else self.failure_url)

    def set_session(self, **kwargs):
        for key, value in kwargs.items():
            self.request.session[key] = value

# 카카오 소셜 로그인
class KakaoLoginCallbackView(KakaoLoginMixin, View):

    success_url = '/registerform'
    failure_url = settings.LOGIN_URL
    model = get_user_model()

    def get(self, request, *args, **kwargs):
        csrf_token = request.GET.get('state')
        code = request.GET.get('code','')
        error_desc = request.GET.get('error', False)
        if error_desc:
            messages.error(request, '로그인에 실패하셨습니다.', extra_tags='danger')
            return HttpResponseRedirect(self.failure_url)
        if not _compare_masked_tokens(csrf_token, request.COOKIES.get('csrftoken')): # state(csrf_token)이 잘못된 경우
            messages.error(request, '잘못된 경로로 로그인 하셨습니다.', extra_tags='danger')
            return HttpResponseRedirect(self.failure_url)
        is_success, error = self.login_with_kakao(code)
        if not is_success:
            messages.error(request, error, extra_tags='danger')
            return HttpResponseRedirect(self.failure_url)
        if not error.is_active:
            if not error.name:
                self.set_session(register_agree=True, social_login=True)
                return HttpResponseRedirect(self.success_url if is_success else self.failure_url)
            else:
                request.session['register_submit'] = True
                return redirect(reverse('registersubmit'))
        if error.is_active:
            login(request, error, 'member.oauth.backends.SocialLoginBackend') # SocialLoginBackend를 통한 인증 시도
            self.success_url = '/'
        return HttpResponseRedirect(self.success_url if is_success else self.failure_url)

    def set_session(self, **kwargs):
        for key, value in kwargs.items():
            self.request.session[key] = value

# 구글 소셜 로그인
class GoogleLoginCallbackView(GoogleLoginMixin, View):

    success_url = '/registerform'
    failure_url = settings.LOGIN_URL
    model = get_user_model()

    def get(self, request, *args, **kwargs):
        csrf_token = request.GET.get('state')
        code = request.GET.get('code')
        if not _compare_masked_tokens(csrf_token, request.COOKIES.get('csrftoken')): # state(csrf_token)이 잘못된 경우
            messages.error(request, '잘못된 경로로 로그인 하셨습니다.', extra_tags='danger')
            return HttpResponseRedirect(self.failure_url)
        is_success, error = self.login_with_google(code)
        if not is_success: # 로그인 실패할 경우
            messages.error(request, error, extra_tags='danger')
            return HttpResponseRedirect(self.failure_url)
        if not error.is_active:
            if not error.name:
                self.set_session(register_agree=True, social_login=True)
                return HttpResponseRedirect(self.success_url if is_success else self.failure_url)
            else:
                request.session['register_submit'] = True
                return redirect(reverse('registersubmit'))
        if error.is_active:
            login(request, error, 'member.oauth.backends.SocialLoginBackend') # SocialLoginBackend를 통한 인증 시도
            self.success_url = '/'
        return HttpResponseRedirect(self.success_url if is_success else self.failure_url)

    def set_session(self, **kwargs):
        for key, value in kwargs.items():
            self.request.session[key] = value