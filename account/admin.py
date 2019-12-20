from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User
from .forms import UserChangeForm

def make_is_active(modeladmin, request, queryset):
    queryset.update(is_active=True)

def make_is_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)
make_is_active.short_description = "가입을 승인합니다."
make_is_inactive.short_description = "계정을 비활성화합니다."


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    list_display = ('name', 'email', 'last_login', 'is_active', 'is_superuser', 'date_joined', 'parish', 'office')
    list_display_links = ('name',)
    list_filter = ('is_active', 'office', 'parish')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email', 'tp', 'birthday')}),
        (_('추가정보'), {'fields': ('parish', 'office')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email', 'tp', 'birthday')}),
        (_('추가정보'), {'fields': ('parish', 'office')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser',)}),
    )
    search_fields = ('tp', 'name', 'username', 'email', 'birthday')
    filter_horizontal = ()
    actions = [make_is_active, make_is_inactive]
# Register your models here.