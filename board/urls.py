from django.urls import path, include
from . import views

app_name = 'board'

urlpatterns = [
    path('<str:pk>', views.Board.as_view(), name='board'),
    path('<str:board_pk>/detail/<str:pk>', views.detail, name='detail'),
    path('<str:board_pk>/write', views.post_write, name="write"),
    path('<str:board_pk>/update/<str:pk>', views.post_update, name="update"),
    path('<str:menu>/delete/<str:pk>', views.post_delete, name="delete")
]