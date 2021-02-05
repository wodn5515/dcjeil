from django.urls import path, include
from . import views

app_name = 'board'

urlpatterns = [
    path('board/<str:pk>', views.Board.as_view(), name='board'),
    path('detail/<str:pk>', views.detail, name='detail'),
    path('write/<str:board_pk>', views.post_write, name="write"),
    path('update/<str:pk>', views.post_update, name="update"),
    path('delete/<str:menu>/<str:pk>', views.post_delete, name="delete")
]