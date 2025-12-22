from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'old_price', 'show_on_main', 'created_at', 'image_preview']
    list_editable = ['price', 'old_price', 'show_on_main']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    list_filter = ['category', 'created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'description', 'category')
        }),
        ('Цены', {
            'fields': ('price', 'old_price')
        }),
        ('Изображение', {
            'fields': ('image_filename', 'image_preview'),
            'description': 'Выберите файл из папки static/main/img/flowers'
        }),
    )
    
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image_filename:
            filename = obj.image_filename.split('/')[-1] if '/' in obj.image_filename else obj.image_filename
            return format_html(
                '<img src="/static/main/img/flowers/{}" style="max-height: 100px; border-radius: 5px;" />',
                filename
            )
        return "Изображение не выбрано"
    image_preview.short_description = 'Предпросмотр'