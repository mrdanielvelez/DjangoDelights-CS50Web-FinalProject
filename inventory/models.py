from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Ingredient(models.Model):
    name = models.CharField(max_length=25)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)

class MenuItem(models.Model):
    item = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)

class RecipeRequirement(models.Model):
    pass

class Purchase(models.Model):
    pass
