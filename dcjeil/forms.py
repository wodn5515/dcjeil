from django import forms
from account.models import User

def email_check(value):
    try:
        User.objects.get(email=value)
    except:
        raise forms.ValidationError("존재하지않는 회원입니다.")

class FindUsernameForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(FindUsernameForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='이메일', help_text="회원가입시 입력한 이메일을 입력해주세요.", validators=[email_check], widget=forms.EmailInput(attrs={
        'autofocus' : 'on'
    }))

class FindPasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(FindPasswordForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label="아이디", widget=forms.TextInput(attrs={
        'autofocus' : 'on'
    }))
    email = forms.EmailField(label='이메일', validators=[email_check], widget=forms.EmailInput(attrs={
    }))

class RegisterForm1(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(RegisterForm1, self).__init__(*args, **kwargs)

    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')
        widget = {
            'username' : forms.TextInput(attrs={
                'autofocus' : 'on'
            }),
        }
        labels = {
            'username' : '아이디',
        }

    def clean(self):
        cleaned_data = super(RegisterForm1, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "비밀번호가 일치하지 않습니다."
            )

class RegisterForm2(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(RegisterForm2, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('name', 'email' ,'tp', 'office' ,'birthday', 'parish', 'address')