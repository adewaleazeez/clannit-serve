from django.contrib import admin
from app.user.models import *
from django.contrib.auth.admin import UserAdmin, Group


class UserAuthAdmin(UserAdmin):
    list_display = ('username','user_id','email','role','estate','country','state','gender','last_login','date_joined')
    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name','image', 'email','gender')}),
        ('User details', {'fields': ('username', 'password')}),
        ('Other Details', {'fields': ('country','country_short','state','ip_address','estate','address','flat_number','mobile_number')}),
        ('User Role', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active','is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Note', {'fields': ('notes',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username', 'password1', 'password2'),
        }),
    )
    list_filter = list()
    search_fields = list()


class RoleManagementAdmin(admin.ModelAdmin):
    list_display = ['role_title']


admin.site.unregister(Group)
admin.site.register(User, UserAuthAdmin)
admin.site.register(RoleManagement, RoleManagementAdmin)
