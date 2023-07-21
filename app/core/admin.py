from django.contrib import admin
from .models import User, UserProfile, Vendor
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    """customizing the user admin class"""
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'vendor_name')
    list_editable = ('is_approved',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(Vendor, VendorAdmin)
