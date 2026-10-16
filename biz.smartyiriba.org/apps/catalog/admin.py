from django.contrib import admin
from .models import Category, Service
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'pricing', 'price', 'currency', 'active')
    list_filter = ('active', 'category', 'pricing')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
