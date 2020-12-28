from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import CreateView
from .forms import NewYearsEveWordForm

# Create your views here.


class NewYearsEveView(SuccessMessageMixin, CreateView):

    form_class = NewYearsEveWordForm
    template_name = "2021words.html"
    success_url = "/"
    success_message = "성공적으로 제출되었습니다."