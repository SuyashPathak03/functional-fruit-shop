from django.db import models
from django.contrib.auth.models import User

class Fruit(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=2085)
    stock = models.IntegerField(default=0)
    objects = models.Manager()

    def __str__(self):
        return f"{self.name} - ₹{self.price}"


class Order(models.Model):
    PAYMENT_METHODS = [
        ("cod", "Cash on Delivery"),
        ("upi", "UPI"),
        ("debit_card", "Debit Card"),
        ("credit_card", "Credit Card"),
    ]

    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    address = models.TextField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    fruit = models.ForeignKey(Fruit, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.fruit.name} (x{self.quantity})"
