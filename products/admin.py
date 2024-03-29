from django.contrib import admin
from .models import Product, Review

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'stock', 'ratings', 'created')
    list_filter = ('category', 'brand')

admin.site.register(Review)