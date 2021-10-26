import json, pytz

from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import Serializer
from django.db import IntegrityError
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import smart_text
from django.views.decorators.csrf import csrf_exempt

from .models import *


class JSONSerializer(Serializer):
    def get_dump_object(self, obj):
        self._current["id"] = smart_text(obj._get_pk_val(), strings_only=True)
        return self._current

def register(request):
    if request.method == "POST":
        full_name = request.POST["full_name"].split(" ")
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=full_name[0], last_name=full_name[-1])
            user.save()
        except IntegrityError:
            return render(request, "inventory/register.html", {
                "message": "Email address is already registered."
            })
        login(request, user)
        return redirect("index")

    return render(request, "inventory/register.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "inventory/login.html", {
                "message": "Invalid credentials."
            })

    return render(request, "inventory/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def index(request):
    return render(request, "inventory/app.html", {
        "item_names": [item.name for item in MenuItem.objects.all()]
    })

@csrf_exempt
@login_required
def app(request, feature):
    if feature == "inventory":
        ingredients = Ingredient.objects.all()
        return JsonResponse(JSONSerializer().serialize(ingredients), safe=False)
    elif feature == "menu":
        items = MenuItem.objects.all()
        return JsonResponse(JSONSerializer().serialize(items), safe=False)
    elif feature == "purchases":
        purchases = Purchase.objects.all().order_by("-timestamp")
        all_purchases = []
        for purchase in purchases:
            all_purchases.append({
                "menu_item": purchase.menu_item.name,
                "timestamp": f"{datetime.strftime(purchase.timestamp, '%b %d, %Y at %I:%M %p %Z')}"
            })
        return JsonResponse(all_purchases, safe=False)
    elif feature == "finances":
        purchases = Purchase.objects.all()
        revenue = 0
        expenses = 0
        for purchase in purchases:
            menu_item = purchase.menu_item
            revenue += float(menu_item.price)
            for requirement in menu_item.requirements.all():
                expenses += requirement.quantity * float(requirement.ingredient.unit_price)
        profit = float(revenue) - expenses
        return JsonResponse({
                "revenue": "{:,.2f}".format(round(revenue, 2)),
                "profit": "{:,.2f}".format(round(profit, 2)),
                "expenses": "{:,.2f}".format(round(expenses, 2))
            })
    else:
        return JsonResponse({"error": "Invalid app feature."}, status=400)

@login_required
def recipes(request, recipe_id):
    try:
        item = MenuItem.objects.get(pk=recipe_id)
    except MenuItem.DoesNotExist:
        return JsonResponse({"error": "Invalid request."}, status=400)
    requirements = []
    for requirement in item.requirements.all():
        requirements.append({
                "name": requirement.ingredient.name,
                "quantity": requirement.quantity,
                "unit": requirement.ingredient.unit
            })
    return JsonResponse({
            "recipe_name": item.name,
            "recipe_price": item.price,
            "recipe_image": item.recipe_image,
            "recipe_link": item.recipe_link,
            "recipe_requirements": requirements
        })

@csrf_exempt
@login_required
def new_item(request):
    if request.method == "POST":
        item_name = request.POST["item_name"]
        price = request.POST["price"]
        image_url = request.POST["image_url"]
        recipe_url = request.POST["recipe_url"]
        item = MenuItem.objects.create(name=item_name, price=price, recipe_image=image_url, recipe_link=recipe_url)
        item.save()
        return redirect("index")

@csrf_exempt
@login_required
def new_ingredient(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    ingredient_name = data.get("ingredient_name")
    quantity = data.get("quantity")
    unit = data.get("unit")
    unit_price = data.get("unit_price")
    ingredient = Ingredient.objects.create(name=ingredient_name, quantity=quantity, unit=unit, unit_price=unit_price)
    ingredient.save()
    return JsonResponse({"message": "Ingredient successfully created."}, status=201)

@csrf_exempt
@login_required
def new_purchase(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    purchased_item = data.get("purchased_item")
    date_time = datetime.strptime(data.get("date_time"), "%Y-%m-%dT%H:%M")
    date_time = date_time.replace(tzinfo=pytz.UTC)
    item = get_object_or_404(MenuItem, name=purchased_item)
    purchase = Purchase.objects.create(user=request.user, menu_item=item, timestamp=date_time)
    purchase.save()
    return JsonResponse({"message": "Purchase successfully added."}, status=201)

@csrf_exempt
@login_required
def delete_ingredient(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("ingredient_id") is not None:
            ingredient_id = data.get("ingredient_id")
            ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
            if data.get("remove") == True:
                ingredient.delete()
            return JsonResponse({"success": "Ingredient successfully deleted"})
        else:
            return JsonResponse({"error": "Invalid request."}, status=400)

