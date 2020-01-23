from django.contrib import admin
from .models import History, Carousel, Server, Pastol, Worship, Community, Welcome
# Register your models here.

class HistoryAdmin(admin.ModelAdmin):
    list_display = ['date', 'content']
    list_display_links = ['content']
    ordering = ['-date',]

admin.site.register(History, HistoryAdmin)
admin.site.register(Carousel)
admin.site.register(Server)
admin.site.register(Pastol)
admin.site.register(Worship)
admin.site.register(Community)
admin.site.register(Welcome)