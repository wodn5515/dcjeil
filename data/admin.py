from django.contrib import admin
from .models import History, Carousel, Community, Popup, Duty, Belong
# Register your models here.

class HistoryAdmin(admin.ModelAdmin):
    list_display = ['date', 'content']
    list_display_links = ['content']
    ordering = ['-date',]
 
admin.site.register(History, HistoryAdmin)
admin.site.register(Carousel)
admin.site.register(Community)
admin.site.register(Popup)
admin.site.register(Duty)
admin.site.register(Belong)