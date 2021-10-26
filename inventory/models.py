from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Ingredient(models.Model):
    name = models.CharField(max_length=25)
    quantity = models.FloatField(validators=[MinValueValidator(0)])
    unit = models.CharField(max_length=10, default="pounds")
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} — {self.quantity} {self.unit} available — ${self.unit_price} per unit"

class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    recipe_image = models.URLField(blank=True, null=True)
    recipe_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} (${self.price})"

class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="requirements")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="recipes")
    quantity = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.quantity} {self.ingredient.unit} of {self.ingredient.name} — {self.menu_item.name}"

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    timestamp = models.DateTimeField(default=timezone.now)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="purchases")

    def __str__(self):
        return f"{self.user} bought {self.menu_item} — {self.timestamp}"
