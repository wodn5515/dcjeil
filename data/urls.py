from django.urls import path, include
from rest_framework import routers
from . import views, api

app_name = 'data'

urlpatterns = [
    path("comments/<str:post>", api.CommentList.as_view()),
]