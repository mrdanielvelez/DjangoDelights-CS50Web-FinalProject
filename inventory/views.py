import json
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import Serializer
from django.db import IntegrityError
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.utils.encoding import smart_text
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt

from .models import *


class JSONSerializer(Serializer):
    def get_dump_object(self, obj):
        self._current["id"] = smart_text(obj._get_pk_val(), strings_only=True)
        return self._current

def index(request):
    return render(request, "inventory/app.html")

def register(request):
    if request.method == "POST":
        full_name = request.POST["full_name"].split(" ")
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=full_name[0], last_name=full_name[-1])
            user.save()
        except IntegrityError:
            print(IntegrityError)
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
            print(purchase)
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

@csrf_exempt
@login_required
def modify(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("ingredient_id") is not None:
            pass
