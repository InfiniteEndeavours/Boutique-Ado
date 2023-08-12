from django.contrib import admin
from .models import Product, Category
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    # Customise how product is displayed in Admin
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


# Registers the Model along with Admin Classes
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
