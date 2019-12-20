from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from .models import User, UserManager

class UserChangeForm(forms.ModelForm):
    # 비밀번호 변경 폼
    password = ReadOnlyPasswordHashField(
        label=_('Password'),
        help_text = ("<a href=\"../password/\">Change</a>.")
    )

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

#사용자 생성 폼
class UserCreationForm(forms.ModelForm):
    pass