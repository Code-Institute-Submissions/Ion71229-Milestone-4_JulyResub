from django.contrib import admin
from .models import MenuItem, Category, OrderModel


class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'name',
        'description',
        'image',
        'price',
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )

admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(OrderModel)