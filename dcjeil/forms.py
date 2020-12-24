from django import forms
from django.contrib.auth.password_validation import validate_password
from member.models import User


class UserCheckForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(UserCheckForm, self).__init__(*args, **kwargs)

    check_pw = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(
        attrs={
            'placeholder':'비밀번호확인'
        }
    ), required=True)
    
class UpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(UpdateForm, self).__init__(*args, **kwargs)

    password = forms.CharField(label="비밀번호", required=False, widget=forms.PasswordInput(), help_text="◈변경 시에만 입력해주세요.<br>◈영문,숫자조합 8-20자")
    confirm_password = forms.CharField(label="비밀번호 확인", required=False, widget=forms.PasswordInput(attrs={
        'autofocus' : 'on'
    }))

    class Meta:
        model = User
        fields = ('name', 'uid', 'email', 'password')
        widget = {
            'uid' : forms.TextInput(attrs={
                'autofocus' : 'on'
            })
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
        user = super(UpdateForm, self).save(commit=False)
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if not password and not confirm_password:
            user.password = self.initial['password']
        else:
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class SocialUpdateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(SocialUpdateForm, self).__init__(*args, **kwargs)
        
    name = forms.CharField(label='이름', widget=forms.TextInput, help_text="◈ 소셜로그인을 통해 가입된 회원입니다.")

    class Meta:
        model = User
        fields = ('name', 'email')
