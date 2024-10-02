from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, OrderItem

class CustomUserAdmin(UserAdmin):
    # Display email in the admin panel
    list_display = ('email', 'username', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', "order")
    search_fields = ('name',)
    
admin.site.register(OrderItem, OrderItemAdmin)