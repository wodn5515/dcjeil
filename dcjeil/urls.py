"""dcjeil URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckeditor_views
from . import views
from board import views as board_views
from member import views as account_views

admin.site.site_header = "덕천제일교회 관리"
admin.site.site_title = "덕천제일교회 관리"
admin.site.index_title = "Home"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("board/", include("board.urls")),
    path("data/", include("data.urls")),
    path("event/", include("event.urls")),
    path("login/", account_views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("login/finduid", account_views.finduid, name="finduid"),
    path("login/findpassword", account_views.findpassword, name="findpassword"),
    path(
        "login/social/naver/callback",
        account_views.NaverLoginCallbackView.as_view(),
        name="naverlogincallback",
    ),
    path(
        "login/social/kakao/callback",
        account_views.KakaoLoginCallbackView.as_view(),
        name="kakaologincallback",
    ),
    path(
        "login/social/google/callback",
        account_views.GoogleLoginCallbackView.as_view(),
        name="Googlelogincallback",
    ),
    path("register", account_views.register, name="register"),
    path("registerform", account_views.registerform, name="registerform"),
    path("registersubmit", account_views.registersubmit, name="registersubmit"),
    path("usercheck", views.usercheck, name="usercheck"),
    path("userupdate", views.userupdate, name="userupdate"),
    path("userresult", views.userresult, name="userresult"),
    path("upload", login_required(ckeditor_views.upload), name="ckeditor_upload"),
    path(
        "browse",
        never_cache(login_required(ckeditor_views.browse)),
        name="ckeditor_browse",
    ),
    path("summernote/", include("django_summernote.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]