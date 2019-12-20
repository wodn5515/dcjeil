from django.urls import path, include
from . import views

urlpatterns = [
    path('<str:pk>', views.board, name='board'),
    path('<str:menu>/<str:pk>', views.detail, name='detail'),
]