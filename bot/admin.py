from django.contrib import admin
from .models import Category, Product, Subcategory
from .models import User


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Subcategory)
admin.site.register(User)
