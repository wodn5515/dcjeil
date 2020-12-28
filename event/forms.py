from django import forms
from .models import NewYearEveWord


class NewYearsEveWordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super(NewYearsEveWordForm, self).__init__(*args, **kwargs)

    class Meta:
        model = NewYearEveWord
        fields = "__all__"
