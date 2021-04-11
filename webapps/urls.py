"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from assistant import views

urlpatterns = [
    path('', views.grocery),
    path('grocery',views.grocery, name='grocery'),
    path('menu',views.menu, name='menu'),
    path('cookbook',views.cookbook, name='cookbook'),
    path('to-do',views.toDo, name='to-do'),
    path('edit',views.edit, name='edit'),
    path('store_grocery',views.swap_list),
    path('repeat_grocery',views.swap_list),
    path('add_grocery',views.add_grocery),
    path('add_stock',views.add_stock),
    path('remove_grocery',views.remove_grocery),
    path('remove_stock',views.remove_stock),
    path('update_lists',views.update_lists),
    path('admin', views.admin_login),
    path('login', views.login_action, name='login'),
    path('select_recipe', views.select_recipe),
    path('edit_recipe', views.edit_recipe, name='edit_recipe'),
]
