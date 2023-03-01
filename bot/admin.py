from django.contrib import admin
from .models import FAQ, Category, Product, Subcategory, User, Cart, CartProduct


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Subcategory)
admin.site.register(User)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(FAQ)
