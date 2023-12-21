from django.db import models
from django.core.validators import RegexValidator

from django.contrib.auth import get_user_model
User = get_user_model()

phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Phone number must be in the format: '+998xxxxxxxxx'."
)


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    for_who = models.CharField(max_length=20,)
    image = models.ImageField(upload_to='images')
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL)
    stock = models.IntegerField(default=0)  # New field for stock

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0

    def reduce_stock(self, quantity):
        if quantity > self.stock:
            return False

        self.stock -= quantity
        self.save()
        return True

    def increase_stock(self, amount):
        self.stock += amount
        self.save()



class View(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(
        validators=[phone_regex], max_length=13, blank=True, null=True)

