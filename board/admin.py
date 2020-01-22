from django.contrib import admin
from .models import Post, PostImage, PostFile, Comment

class PostImageInline(admin.StackedInline):
    model = PostImage
    extra = 0

class PostFileInline(admin.StackedInline):
    model = PostFile
    extra = 0

class Postadmin(admin.ModelAdmin):
    list_display = ['title', 'div', 'upload_date', 'views']
    list_filter = ['div', 'published']
    list_per_page = 20
    inlines = [PostImageInline, PostFileInline]

class PostImageadmin(admin.ModelAdmin):
    list_display = ['get_imagename','get_div', 'get_title']
    list_filter = ['post__div']
    search_fields = ['image']

    def get_imagename(self, obj):
        return obj.image.name.split('/')[-1]
    def get_div(self, obj):
        return obj.post.get_div_display()
    def get_title(self, obj):
        return obj.post.title
    get_imagename.short_description = '파일명'
    get_div.short_description = '구분'
    get_title.short_description = '제목'

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
admin.site.register(PostImage, PostImageadmin)
admin.site.register(Comment)
admin.site.register(PostFile, PostFileadmin)