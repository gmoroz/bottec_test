from django.db import models
from django.contrib.auth.models import AbstractUser
from bot.tg_bot.managers import CustomUserManager


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
    price = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    async def caption(self):
        return "\n".join((self.name, f"Цена: {self.price}₽", self.description))


class User(AbstractUser):
    tg_id = models.BigIntegerField(unique=True)
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"

    def __str__(self):
        return f"{self.product.name} {self.quantity} шт."


class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField(default="На данный вопрос пока что нет ответа")

    class Meta:
        verbose_name = "Вопрос и ответ"
        verbose_name_plural = "Вопросы и ответы"

    def __str__(self):
        return self.question
