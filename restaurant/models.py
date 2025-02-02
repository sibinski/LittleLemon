from django.db import models

# Create your models here.
class MenuItems(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    inventory = models.PositiveIntegerField(db_index=True)

    def get_item(self):
        return f'{self.title} : {str(self.price)}'

class Booking(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    guests = models.PositiveIntegerField(default=1, db_index=True)
    table = models.PositiveIntegerField(default=1, db_index=True)
    date = models.DateTimeField(db_index=True)

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)


    def __str__(self) -> str:
        return self.title

class User(models.Model):
    url = models.URLField()
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    groups = models.CharField(max_length=255)

class Menu(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(default=1, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.title}:{str(self.price)}'

