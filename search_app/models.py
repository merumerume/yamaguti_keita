from django.db import models
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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1) 
    # 1はカテゴリID
    def __str__(self):
        return self.name



#追加
#ブックマーク
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
#ログイン
