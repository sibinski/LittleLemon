from pickletools import read_string4
from typing_extensions import ReadOnly
from rest_framework.exceptions import ValidationError 
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)


    def __str__(self) -> str:
        return self.title

class MenuItems(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)

    def __str__(self) -> str:
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ('menuitem', 'user')
    
    def save(self, *args, **kwargs):
        self.price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

def clean(self):
        # Optional: Custom validations for additional integrity
        if self.quantity <= 0:
            raise ValidationError({'quantity': "Quantity must be greater than 0."})
        if self.unit_price < 0:
            raise ValidationError({'unit_price': "Unit price must be non-negative."})

def __str__(self):
    return f"{self.user.username}'s cart - {self.menuitem.name} (x{self.quantity})"

class Order(models.Model):
    PENDING = 'PENDING'
    SHIPPED = 'SHIPPED'
    DELIVERED = 'DELIVERED'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(db_index=True)


class OrderItem(models.Model):
    order = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('order', 'menuitem')



