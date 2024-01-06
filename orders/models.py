from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class OrderStatus(models.TextChoices):
    PENDING = 'Pending'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELLED = 'Cancelled'

class PaymentStatus(models.TextChoices):
    PENDING = 'Pending'
    PAID = 'Paid'

class PaymentMethod(models.TextChoices):
    CREDIT_CARD = 'Credit Card'
    CASH = 'Cash'

class Order(models.Model):
    user = models.ForeignKey(User, null = True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=200, default='', blank = False)
    street = models.CharField(max_length=200, default='', blank = False)
    state = models.CharField(max_length=200, default='', blank = False)
    country = models.CharField(max_length=200, default='', blank = False)
    zip_code = models.CharField(max_length=200, default='', blank = False)
    phone = models.CharField(max_length=200, default='', blank = False)
    total_amount = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    status = models.CharField(max_length=40, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    payment_status = models.CharField(max_length=40, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_method = models.CharField(max_length=40, choices=PaymentMethod.choices, default=PaymentMethod.CREDIT_CARD)


    def __str__(self):
        return f'Order #{self.id} - {self.user.username}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name = 'items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name = 'order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField( max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.id} - {self.product.name}'