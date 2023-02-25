from django.db import models


class BaseModel(models.Model):
    name = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.name


class Category(BaseModel):
    pass


class Subcategory(BaseModel):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )


class Product(BaseModel):
    description = models.TextField()
    image = models.ImageField()
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, related_name="products"
    )
