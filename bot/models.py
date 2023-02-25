from django.db import models


class BaseModel(models.Model):
    name = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Category(BaseModel):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Subcategory(BaseModel):
    parent_category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


class Product(BaseModel):
    description = models.TextField()
    image = models.ImageField()
    sub_category = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, related_name="products"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
