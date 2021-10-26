"""djangodelights URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from inventory import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("app/<str:feature>", views.app, name="app"),
    path("recipes/<int:recipe_id>", views.recipes, name="recipes"),
    path("new_item/", views.new_item, name="new_item"),
    path("new_ingredient/", views.new_ingredient, name="new_ingredient"),
    path("delete_ingredient/", views.delete_ingredient, name="delete_ingredient"),
    path("new_purchase/", views.new_purchase, name="new_purchase"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
