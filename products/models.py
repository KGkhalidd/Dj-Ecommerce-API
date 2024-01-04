from django.db import models
from django.contrib.auth.models import User

class Category(models.TextChoices):
    ELECTRONICS = 'Electronics'
    CLOTHING = 'Clothing'
    BOOKS = 'Books'
    SPORTS = 'Sports'
    HOME = 'Home'
    OTHER = 'Other'

class Product(models.Model):
    name = models.CharField(max_length=200, default='', blank = False)
    description = models.TextField(max_length=1000 ,default='', blank = False)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    brand = models.CharField(max_length=200, default='', blank = False)
    category = models.CharField(max_length=40, choices=Category.choices, default=Category.OTHER)
    ratings = models.DecimalField( max_digits=5, decimal_places=2, default=0.00)
    stock = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null = True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, related_name = 'reviews' ,on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, null = True, on_delete=models.SET_NULL)
    comment = models.TextField(max_length=1000 ,default='', blank = False)
    rating = models.DecimalField( max_digits=5, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.comment