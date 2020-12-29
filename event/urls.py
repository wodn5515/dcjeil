from django.urls import path, include
from . import views

app_name = "event"

urlpatterns = [
    path("2021words", views.NewYearsEveView.as_view(), name="newyearseve"),
    path("newyearspirit", views.NewYearSpirit.as_view(), name="newyearspirit"),
]
