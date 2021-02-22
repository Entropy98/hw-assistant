from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
# Create your views here.

def home(request):
    if(request.method == 'GET'):
        return render(request,"assistant/index.html")

@csrf_exempt
def add_grocery(request):
    if(request.method == 'GET'):
        return render(request,"assistant/index.html")
    if('quantity' in request.POST && 'grocery' in request.POST):
        try:
            #known grocery
            grocery = GroceryItem.objects.get(name=request.POST['grocery'])
        except:
            #new grocery
            grocery = GroceryItem(name=request.POST['grocery'], category='misc')
            grocery.save()
        grocery_list = ListItem.objects.get(name='grocery', category=grocery.category)
        grocery_list.checklist.add(grocery)
        grocery_list.save()
    return order(request)
