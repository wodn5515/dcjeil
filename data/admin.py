from django.contrib import admin
from .models import History, Carousel, Server, Pastol, Worship, Community, Welcome, Mainmenu, Submenu
# Register your models here.

class HistoryAdmin(admin.ModelAdmin):
    list_display = ['date', 'content']
    list_display_links = ['content']
    ordering = ['-date',]

class SubmenuInline(admin.StackedInline):
    model = Submenu
    extra = 0

class MenuAdmin(admin.ModelAdmin):
    list_display = ['name',]
    ordering = ['order']
    inlines = [SubmenuInline]

admin.site.register(History, HistoryAdmin)
admin.site.register(Carousel)
admin.site.register(Server)
admin.site.register(Pastol)
admin.site.register(Worship)
admin.site.register(Community)
admin.site.register(Welcome)
admin.site.register(Mainmenu, MenuAdmin)