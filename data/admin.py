from django.contrib import admin
from .models import History
# Register your models here.

class HistoryAdmin(admin.ModelAdmin):
    list_display = ['date', 'content']
    list_display_links = ['content']
    ordering = ['-date',]

admin.site.register(History, HistoryAdmin)