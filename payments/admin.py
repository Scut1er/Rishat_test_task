from django.contrib import admin
from .models import Item, Order, OrderItem, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    list_filter = ('price',)
    search_fields = ('name', 'description')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'get_total_price')
    list_filter = ('created_at',)
    inlines = [OrderItemInline]
    
    def get_total_price(self, obj):
        return f"${obj.get_total_price()}"
    get_total_price.short_description = "Общая стоимость"


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent', 'stripe_coupon_id')
    search_fields = ('name',)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent', 'stripe_tax_rate_id')
    search_fields = ('name',)
