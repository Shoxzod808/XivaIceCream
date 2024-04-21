from django.contrib import admin
from .models import Product, Inventory, Order, OrderDetail, User

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'flavor', 'expiration_date', 'manufacture_date')

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'location')
    list_filter = ('location',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_ordered', 'status', 'delivery_date')
    list_filter = ('status',)

class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    list_filter = ('order',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role')
    list_filter = ('role',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(User, UserAdmin)
