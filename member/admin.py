from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from .models import User, AdminPermissionGroup, BoardPermissionGroup
from .forms import UserChangeForm, UserCreationForm

def make_is_active(modeladmin, request, queryset):
    queryset.update(is_active=True)

def make_is_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)
make_is_active.short_description = "가입을 승인합니다."
make_is_inactive.short_description = "계정을 비활성화합니다."


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    list_display = ('name', 'last_login', 'is_active', 'is_superuser', 'is_registered', 'date_joined',)
    list_display_links = ('name',)
    list_filter = ('belong', 'duty', 'is_active', 'is_superuser', 'is_staff',)
    fieldsets = (
        (_('회원정보'), {'fields': ('uid', 'password',)}),
        (_('Personal info'), {'fields': ('name', 'email',)}),
        (_('추가정보'), {'fields': ('is_registered', 'belong', 'duty',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser', 'is_staff', 'adminpermissiongroups', 'boardpermissiongroups',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('uid', 'password',)}),
        (_('Personal info'), {'fields': ('name', 'email',)}),
        (_('추가정보'), {'fields': ('is_registered', 'belong', 'duty',)})
    )
    search_fields = ('name', 'uid',)
    filter_horizontal = ()
    ordering = ['uid',]
    actions = [make_is_active, make_is_inactive]

@admin.register(AdminPermissionGroup)
class AdminPermissionGroupAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'permissions':
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs['queryset'] = qs.select_related('content_type')
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)
    
@admin.register(BoardPermissionGroup)
class BoardPermissionGroupAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
        
admin.site.unregister(Group)