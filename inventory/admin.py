from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Ingredient)
admin.site.register(MenuItem)
admin.site.register(RecipeRequirement)
admin.site.register(Purchase)
