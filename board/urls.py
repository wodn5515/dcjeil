from django.urls import path, include
from . import views

app_name = 'board'

urlpatterns = [
    path('<str:pk>', views.board, name='board'),
    path('<str:menu>/detail/<str:pk>', views.detail, name='detail'),
    path('<str:menu>/write', views.post_write, name="write"),
    path('<str:menu>/update/<str:pk>', views.post_update, name="update"),
    path('<str:menu>/delete/<str:pk>', views.post_delete, name="delete")
]