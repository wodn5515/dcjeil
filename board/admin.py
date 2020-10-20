from django.contrib import admin
from .models import Post, PostFile, Comment, Posttag

class PostFileInline(admin.StackedInline):
    model = PostFile
    extra = 0

class Postadmin(admin.ModelAdmin):
    list_display = ['title', 'get_div', 'upload_date', 'views']
    exclude = ['image',]
    list_filter = ['div__name', 'published']
    list_per_page = 20
    inlines = [PostFileInline]
    
    def get_div(self, obj):
        return obj.div.name
    get_div.short_description = '메뉴'
    

class PostFileadmin(admin.ModelAdmin):
    list_display = ['get_imagename', 'get_div', 'get_title']
    list_filter = ['post__div__name']
    search_fields = ['file']

    def get_imagename(self, obj):
        return obj.file.name.split('/')[-1]
    def get_div(self, obj):
        return obj.post.div.name
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