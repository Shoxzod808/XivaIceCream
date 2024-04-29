from django.contrib import admin
from .models import Product, InventoryProduct, Inventory, Driver, OrderProduct, Order, Payment, Refund, RefundProduct

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'case', 'count')
    search_fields = ('name',)

class InventoryProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'count', 'inventory')
    search_fields = ('product__name',)
    list_filter = ('inventory',)

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('created_date',)
    date_hierarchy = 'created_date'

class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'auto')
    search_fields = ('name', 'phone')

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'count', 'order')
    search_fields = ('product__name',)
    list_filter = ('order',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('created_date', 'driver', 'cash')
    date_hierarchy = 'created_date'
    search_fields = ('driver__name',)



# Регистрация моделей
admin.site.register(Product, ProductAdmin)
admin.site.register(InventoryProduct, InventoryProductAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Order, OrderAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('driver', 'cash', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('order__id',)

class RefundAdmin(admin.ModelAdmin):
    list_display = ('created_date', 'order', 'cash')
    list_filter = ('created_date',)
    search_fields = ('order__id',)

class RefundProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'count', 'refund')
    search_fields = ('product__name', 'refund__id')

admin.site.register(Payment, PaymentAdmin)
admin.site.register(Refund, RefundAdmin)
admin.site.register(RefundProduct, RefundProductAdmin)