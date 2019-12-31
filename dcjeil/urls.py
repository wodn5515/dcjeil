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
from django.urls import path, include
from . import views
from board import views as board_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('board/', include('board.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/finduid', views.finduid, name='finduid'),
    path('login/finduid2', views.finduid2, name='finduid2'),
    path('login/findpassword', views.findpassword, name='findpassword'),
    path('login/findpassword2', views.findpassword2, name='findpassword2'),
    path('register', views.register, name='register'),
    path('registerform', views.registerform, name='registerform'),
    path('test', views.test, name='test'),
    path('comments/<str:pk>', board_views.comments, name='comments'),
    path('comments/<str:pk>/delete', board_views.comment_delete, name='comment_delete')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
