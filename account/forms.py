from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from .choice import *
from .models import User, UserManager

        
def email_user_check(value):
    try:
        User.objects.get(email=value)
    except:
        raise forms.ValidationError("존재하지않는 회원입니다.")


class UserChangeForm(forms.ModelForm):
    # 비밀번호 변경 폼
    password = ReadOnlyPasswordHashField(
        label=_('Password'),
        help_text = ("<a href=\"../password/\">Change</a>.")
    )

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

#사용자 생성 폼
class UserCreationForm(forms.ModelForm):
    
    password = forms.CharField(label = _('Password'), widget = forms.PasswordInput())

    class Meta:
            model = User
            fields = ('uid', 'password', 'name', 'email', 'tp', 'birthday', 'parish', 'office')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.email = UserManager.normalize_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class FinduidForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(FinduidForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='이메일', help_text="회원가입시 입력한 이메일을 입력해주세요.", validators=[email_user_check], widget=forms.EmailInput(attrs={
        'autofocus' : 'on'
    }))

class FindPasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(FindPasswordForm, self).__init__(*args, **kwargs)

    uid = forms.CharField(label="아이디", widget=forms.TextInput(attrs={
        'autofocus' : 'on'
    }))
    email = forms.EmailField(label='이메일', validators=[email_user_check], widget=forms.EmailInput(attrs={
    }))

class RegisterForm1(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(RegisterForm1, self).__init__(*args, **kwargs)

    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('uid', 'password')
        widget = {
            'uid' : forms.TextInput(attrs={
                'autofocus' : 'on'
            }),
        }
        labels = {
            'uid' : '아이디',
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        return confirm_password

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm1, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        return user


class RegisterForm2(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(RegisterForm2, self).__init__(*args, **kwargs)

    birthday = forms.DateField(label="생년월일", required=False, widget=forms.SelectDateWidget(empty_label=("-년도-", "--월--", "--일--"), years=range(2020, 1900, -1)))

    class Meta:
        model = User
        fields = ('name', 'email', 'tp', 'birthday', 'office',)
        help_texts = {
            'tp': "'-'를 제외한 숫자만 입력해주세요."
        }