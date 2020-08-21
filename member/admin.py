from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User
from .forms import UserChangeForm, UserCreationForm

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
    add_form = UserCreationForm
    list_display = ('name', 'last_login', 'is_active', 'is_superuser', 'date_joined',)
    list_display_links = ('name',)
    list_filter = ('is_active',)
    fieldsets = (
        (None, {'fields': ('uid', 'password',)}),
        (_('Personal info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser', 'is_staff', 'groups',)}),
        (_('게시판 권한'), {'fields': ('has_permission',)})
    )
    add_fieldsets = (
        (None, {'fields': ('uid', 'password',)}),
        (_('Personal info'), {'fields': ('name',)}),
    )
    search_fields = ('name', 'uid',)
    filter_horizontal = ()
    ordering = ['uid',]
    actions = [make_is_active, make_is_inactive]
# Register your models here.