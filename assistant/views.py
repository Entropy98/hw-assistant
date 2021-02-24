from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from assistant.models import *

import json
# Create your views here.

#categories of lists
lists=['produce','alcohol','pantry','dairy','misc']

def home(request):
    context={'categories': lists}
    if(request.method == 'GET'):
        return render(request,"assistant/index.html", context)
    return render(request,"assistant/index.html", context)

@csrf_exempt
def add_grocery(request):
    if(request.method == 'GET'):
        return render(request,"assistant/index.html")
    body = json.loads(request.body.decode('utf-8'))
    if(('quantity' in body) and ('grocery' in body)):
        try:
            #known grocery
            grocery = GroceryItem.objects.get(name=body['grocery'])
            grocery.quantity += int(body['quantity'])
        except:
            #new grocery
            grocery = GroceryItem(  name=body['grocery'],
                                    category='misc',
                                    quantity=body['quantity'])
        grocery.save()
    return update_lists(request)

def update_lists(request):
    json_response = []
    list_obj = {}
    for list_type in lists:
        list_type_obj={}
        for grocery in GroceryItem.objects.filter(category=list_type):
            if(grocery.quantity > 0):
                list_type_obj[grocery.name] = grocery.quantity
        list_obj[list_type] = list_type_obj
    json_response.append(list_obj)
    response_json = json.dumps(json_response)
    response = HttpResponse(response_json, content_type='application/json')
    return response

