from django.contrib import admin
from .models import Product, Category,ProductAlbum, Stock

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductAlbum)
admin.site.register(Stock)