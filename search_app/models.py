from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
#追加

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1) 
    # 1はカテゴリID
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")  # Productと1対多の関係
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # レビュー投稿者
    rating = models.PositiveIntegerField(default=1)  # 1〜5の評価
    comment = models.TextField()  # レビュー内容
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時

    def __str__(self):
        return f"{self.user.username} - {self.rating}★"



