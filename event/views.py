from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import CreateView
from .forms import NewYearsEveWordForm, NewYearSpiritForm

# Create your views here.


class EventMixin(SuccessMessageMixin, CreateView):

    success_url = "/"
    success_message = "성공적으로 제출되었습니다."
    template_name = "event_form.html"
    title = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context


class NewYearsEveView(EventMixin):

    form_class = NewYearsEveWordForm
    title = "송구영신예배 말씀뽑기"


class NewYearSpirit(EventMixin):

    form_class = NewYearSpiritForm
    title = "새해 새마음 세이레 이벤트"