from django.contrib import admin
from .models import Mainmenu, Submenu, FixedMenu

# Register your models here.
class SubmenuInline(admin.StackedInline):
    model = Submenu
    extra = 0

class MaunmenuAdmin(admin.ModelAdmin):
    list_display = ['name',]
    ordering = ['order']
    inlines = [SubmenuInline]

class SubmenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'mainmenu',]
    list_filter = ['mainmenu']
    
class FixedmenuAdmin(admin.ModelAdmin):
    list_filter = ['menu',]
   
   
admin.site.register(FixedMenu, FixedmenuAdmin)
admin.site.register(Mainmenu, MaunmenuAdmin)
admin.site.register(Submenu, SubmenuAdmin)