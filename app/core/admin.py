from django.contrib import admin
from .models import User, UserProfile, Vendor, Category, Product
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


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'vendor', 'updated_at')
    search_fields = ('category_name', 'vendor__vendor_name')
    prepopulated_fields = {'slug': ('category_name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_title', 'category', 'vendor',
                    'price', 'is_available', 'updated_at')
    prepopulated_fields = {'slug': ('product_title',)}
    search_fields = ('product_title', 'category__category_name',
                     'vendor__vendor_name', 'price')
    list_filter = ('is_available',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
