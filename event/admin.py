from django.contrib import admin
from django.utils.html import mark_safe
from .models import NewYearEveWord

# Register your models here.


@admin.register(NewYearEveWord)
class NewYearEveWordAdmin(admin.ModelAdmin):
    list_display = ("__str__", "file_link")

    def file_link(self, obj):
        if obj.words:
            return mark_safe(f"<a href='{obj.words.url}' download>다운로드</a>")
        else:
            return "첨부파일 없음"

    file_link.allow_tags = True
    file_link.short_description = "파일 다운로드"
