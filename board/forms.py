from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Comment, Post, PostFile, Posttag
import re, datetime

class AddCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)

class PostWriteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(PostWriteForm, self).__init__(*args, **kwargs)

    title = forms.CharField(label="제목", widget=forms.TextInput(attrs={'class':'required full'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'required'}), label="내용", required=False)

    class Meta:
        model = Post
        fields = ('title', 'content',)

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content == '':
            raise forms.ValidationError('내용을 입력해주세요.')
        return content

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title == '':
            raise forms.ValidationError('제목을 입력해주세요.')
        return title

class PostSuperuserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(PostSuperuserForm, self).__init__(*args, **kwargs)

    title = forms.CharField(label="제목", widget=forms.TextInput(attrs={'class':'required'}))
    tag = forms.ModelChoiceField(label="태그", queryset=Posttag.objects.all(), widget=forms.Select(attrs={'class':'tag'}), required=False)
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'required', 'id':'editor'}), label="내용", required=False)
    date = forms.DateField(label="일시", required=False, widget=forms.SelectDateWidget(empty_label=("-년도-", "--월--", "--일--"), years=range(datetime.datetime.now().year, 2000, -1)), help_text='◈ 설교, 찬양, 기도에만 작성하세요.')
    preacher = forms.CharField(label="설교자", required=False, widget=forms.TextInput(attrs={'class':'half', 'placeholder':'ex)김대환 목사'}), help_text='◈ 설교에만 작성하세요.')
    words = forms.CharField(label="말씀", required=False, widget=forms.TextInput(attrs={'class':'half', 'placeholder':'ex)창세기 1:1~10'}), help_text='◈ 설교에만 작성하세요.')
    video = forms.CharField(label="동영상", required=False, widget=forms.TextInput(attrs={'class':'half'}), help_text='◈ 유튜브 주소를 입력하세요.')
    notice = forms.BooleanField(label="공지사항", required=False)

    class Meta:
        model = Post
        fields = ('notice', 'tag', 'title', 'date', 'preacher', 'words', 'video', 'content')

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title == '':
            raise forms.ValidationError('제목을 입력해주세요.')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        video = self.cleaned_data.get('video')
        if content == '' and video == '':
            raise forms.ValidationError('내용이나 동영상을 입력해주세요.')
        return content


PostFileFormset = forms.modelformset_factory(PostFile, extra=0, max_num=5, fields=('file',), can_delete=True)