from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext_lazy as _
from .choice import *
from .models import User, UserManager

        
def uid_check(value):
    try:
        User.objects.get(uid=value)
    except:
        raise forms.ValidationError("존재하지않는 회원입니다.")
        
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
            fields = ('uid', 'password', 'name', 'email')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# 로그인 폼
class LoginForm(forms.Form):
    uid = forms.CharField(widget=forms.TextInput(
        attrs={
            'autofocus' : 'off',
            'placeholder' : '아이디'
        }
    ), required=False)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'autofocus' : 'off',
            'placeholder' : '비밀번호'
        }
    ), required=False)

    def clean(self):
        uid = self.cleaned_data.get('uid')
        password = self.cleaned_data.get('password')
        if uid == None:
            raise forms.ValidationError("아이디를 입력해주세요.")
        if password == None:
            raise forms.ValidationError("비밀번호를 입력해주세요.")
        user = authenticate(uid=uid, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("가입하지 않은 아이디이거나, 잘못된 비밀번호입니다.")
        return self.cleaned_data

    def login(self, request):
        uid = self.cleaned_data.get('uid')
        password = self.cleaned_data.get('password')
        user = authenticate(uid=uid, password=password)
        return user

class FinduidForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(FinduidForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='이메일', help_text="회원가입시 입력한 이메일을 입력해주세요.", validators=[email_user_check], widget=forms.EmailInput(attrs={
        'autofocus' : 'on',
        'placeholder' : '이메일'
    }))

class FindPasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(FindPasswordForm, self).__init__(*args, **kwargs)

    uid = forms.CharField(label="아이디", validators=[uid_check], widget=forms.TextInput(attrs={
        'autofocus' : 'on',
        'placeholder' : '아이디'
    }))
    email = forms.EmailField(label='이메일', help_text="회원가입시 입력한 이메일을 입력해주세요.", validators=[email_user_check], widget=forms.EmailInput(attrs={
        'placeholder' : '이메일'
    }))

class CertificationNumberForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CertificationNumberForm, self).__init__(*args, **kwargs)

    cert = forms.CharField(label="인증번호", widget=forms.TextInput(attrs={
        "placeholder": "인증번호"
    }))


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(RegisterForm, self).__init__(*args, **kwargs)

    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput(), help_text="◈ 영문,숫자조합 8-20자")
    confirm_password = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('uid', 'password', 'confirm_password', 'name', 'email', 'tp', 'is_registered')
        widget = {
            'uid' : forms.TextInput(attrs={
                'autofocus' : 'on'
            }),
        }
        labels = {
            'uid' : '아이디',
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            validate_password(password)
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password:
            try:
                validate_password(password)
            except:
                pass
            else:
                if password != confirm_password:
                    raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        return confirm_password

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        return user