from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

class ProfileInlime(admin.StackedInline):
    model = UserProfile
    fields=[field.name for field in UserProfile._meta.get_fields()]
    extra = 0  
    
class UserItemsInline(admin.TabularInline):
    model = UserItems
    fields=['product', 'count', 'active']
    extra = 0

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('steamID', "ban_status")
    list_display_links = ('steamID', )
    search_fields = ['steamID']
    inlines = [UserItemsInline, ProfileInlime]

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',) 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'item_level', 'can_upgrade')
    list_display_links = ('name', )
    
    # def get_photo(self, obj):
    #     if obj.image:
    #         return mark_safe(f'<img src="{obj.image.url}" width="50"')
    #     else:
    #         return "Нет фото"

    # get_photo.short_description = "Фото"