from django.contrib import admin
from .models import Product, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'created_at', 'updated_at']
    list_filter = ['category', 'created_at', 'updated_at']
    search_fields = ['name', 'description']

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)