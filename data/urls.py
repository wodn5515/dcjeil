from django.urls import path, include
from . import views

app_name = 'data'

urlpatterns = [
    path('history', views.history, name="history"),
    path('community/<str:div>', views.community, name='community'),
]