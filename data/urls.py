from django.urls import path, include
from . import views

app_name = 'data'

urlpatterns = [
    path('history', views.history, name="history"),
    path('server', views.server, name="server"),
    path('pastol', views.pastol, name="pastol"),
    path('worship', views.worship, name="worship"),
    path('community/<str:div>', views.community, name='community'),
    path('welcome', views.welcome, name="welcome"),
]
