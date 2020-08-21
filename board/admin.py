from django.contrib import admin
from .models import Post, PostFile, Comment, Posttag

class PostFileInline(admin.StackedInline):
    model = PostFile
    extra = 0

class Postadmin(admin.ModelAdmin):
    list_display = ['title', 'div', 'upload_date', 'views']
    exclude = ['image',]
    list_filter = ['div', 'published']
    list_per_page = 20
    inlines = [PostFileInline]

class PostFileadmin(admin.ModelAdmin):
    list_display = ['get_imagename','get_div', 'get_title']
    list_filter = ['post__div']
    search_fields = ['file']

    def get_imagename(self, obj):
        return obj.file.name.split('/')[-1]
    def get_div(self, obj):
        return obj.post.get_div_display()
    def get_title(self, obj):
        return obj.post.title
    get_imagename.short_description = '파일명'
    get_div.short_description = '구분'
    get_title.short_description = '제목'

# Register your models here.
admin.site.register(Post, Postadmin)
admin.site.register(Posttag)
admin.site.register(Comment)
admin.site.register(PostFile, PostFileadmin)