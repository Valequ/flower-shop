from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Order, OrderItem

try:
    from django.contrib.auth.models import User
    admin.site.unregister(User)
except:
    pass

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 
        'email', 
        'full_name',
        'role',
        'phone',
        'is_staff',
        'is_superuser',
        'is_active',
        'date_joined'
    )
    
    list_filter = (
        'role',
        'is_staff',
        'is_superuser',
        'is_active',
        'agreed_to_terms'
    )
    
    search_fields = (
        'username',
        'email',
        'full_name',
        'phone'
    )
    # То, что можно отредактировать
    list_editable = (
        'role',
        'is_active',
        'is_staff'
    )
    
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Персональная информация', {
            'fields': ('full_name', 'email', 'phone', 'avatar')
        }),
        ('Роль и права', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Соглашения', {
            'fields': ('agreed_to_terms', 'agreed_to_offer', 'agreed_to_privacy')
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    # Поля при создании нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role'),
        }),
        ('Персональная информация', {
            'classes': ('wide',),
            'fields': ('full_name', 'email', 'phone'),
        }),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'payment_method']
    inlines = [OrderItemInline]
    search_fields = ['order_number', 'user__username', 'delivery_address']
