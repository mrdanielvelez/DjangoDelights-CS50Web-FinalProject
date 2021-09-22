from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from models import *

def index(request):
    return render("inventory/index.html")

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
        redirect("index")

    return render("inventory/register.html")

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            redirect("inventory")
        else:
            return render("inventory/login.html", {
                "message": "Invalid credentials."
            })

    return render("inventory/login.html")

def logout(request):
    logout(request)
    return redirect("inventory/index.html")

@login_required
def inventory(request):
    ingredients = Ingredient.objects.all()
    return render(request, "inventory/inventory.html", {
        "ingredients": ingredients
    })

@login_required
def menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, "inventory/menu.html", {
        "menu_items": menu_items
    })

@login_required
def purchases(request):
    purchases = Purchase.objects.all()
    return render(request, "inventory/purchases.html", {
        "purchases": purchases
    })

@login_required
def finances(request):
    purchases = Purchase.objects.all()
    revenue = 0
    cost = 0
    for purchase in purchases:
        menu_item = purchase.menu_item
        revenue += menu_item.price
        for requirement in menu_item.requirements:
            cost += requirement.quantity * requirement.ingredient.unit_price
    profit = revenue - cost
    print(revenue, cost, profit)
    return render(request, "inventory/finances.html", {
        "revenue": revenue,
        "cost": cost,
        "profit": profit
    })
    
