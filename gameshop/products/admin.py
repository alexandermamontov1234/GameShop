from django.contrib import admin
from products.models import Product, Category, Review


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Review)

