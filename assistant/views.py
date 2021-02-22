from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from assistant.models import *

import json
# Create your views here.

def home(request):
    context = {}
    groceries = GroceryItem.objects.all()
    for grocery in groceries:
        if(grocery.quantity > 0):
            grocery_list.append(grocery)
    context['grocery_list']=groceries
    if(request.method == 'GET'):
        return render(request,"assistant/index.html",context)
    return render(request,"assistant/index.html",context)

@csrf_exempt
def add_grocery(request):
    if(request.method == 'GET'):
        return render(request,"assistant/index.html")
    if(('quantity' in request.POST) and ('grocery' in request.POST)):
        try:
            #known grocery
            grocery = GroceryItem.objects.get(name=request.POST['grocery'])
            grocery.quantity += int(request.POST['quantity'])
        except:
            #new grocery
            grocery = GroceryItem(  name=request.POST['grocery'],
                                    category='misc',
                                    quantity=request.POST['quantity'])
            grocery.save()
    return order(request)
