from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from assistant.models import *

import json
# Create your views here.

#categories of lists
lists=['produce','alcohol','pantry','dairy','misc']

def grocery(request):
    context={'categories': lists}
    if(request.method == 'GET'):
        return render(request,"assistant/grocery.html", context)
    return render(request,"assistant/grocery.html", context)

def menu(request):
    pass

def toDo(request):
    pass

def extractNum(s):
    res = ''
    for c in s:
        if(c.isnumeric()):
            res = res + c
    return int(res)

@csrf_exempt
def swap_list(request):
    if(request.method == 'GET'):
        return render(request,"assistant/grocery.html")
    if(('quantity' in request.POST) and ('grocery' in request.POST)):
        grocery = GroceryItem.objects.get(name=request.POST['grocery'])
        grocery.quantity = grocery.quantity * -1
        grocery.save()
    return update_lists(request)

@csrf_exempt
def add_stock(request):
    if(request.method == 'GET'):
        return render(request,"assistant/grocery.html")
    body = json.loads(request.body.decode('utf-8'))
    for word in body:
        word = word.replace(' ','')
    if(('quantity' in body) and ('grocery' in body)):
        try:
            #known grocery
            grocery = GroceryItem.objects.get(name=body['grocery'])
            if(grocery.quantity > 0):#in stock list
                grocery.quantity += int(body['quantity'])
            else:
                grocery.quantity = int(body['quantity'])
        except:
            #new grocery
            grocery = GroceryItem(  name=body['grocery'],
                                    category='misc',
                                    quantity=extractNum(body['quantity']))
        grocery.save()
    return update_lists(request)

@csrf_exempt
def remove_stock(request):
    if(request.method == 'GET'):
        return render(request,"assistant/grocery.html")
    body = json.loads(request.body.decode('utf-8'))
    for word in body:
        word = word.replace(' ','')
    if(('quantity' in body) and ('grocery' in body)):
        try:
            #known grocery
            grocery = GroceryItem.objects.get(name=body['grocery'])
            quant = int(body['quantity'])
            if(grocery.quantity > 0):#in stock list
                if(quant <= grocery.quantity):
                    grocery.quantity -= quant
                else:
                    grocery.quantity = 0
                grocery.save()
        except:
            #grocery not found
            pass
    return update_lists(request)

@csrf_exempt
def add_grocery(request):
    if(request.method == 'GET'):
        return render(request,"assistant/grocery.html")
    body = json.loads(request.body.decode('utf-8'))
    print(body)
    if(('quantity' in body) and ('grocery' in body)):
        try:
            #known grocery
            grocery = GroceryItem.objects.get(name=body['grocery'])
            if(grocery.quantity < 0):#in grocery list
                grocery.quantity -= int(body['quantity'])
            else:#remove from stock and add to grocery list
                grocery.quantity = -1*int(body['quantity'])
        except:
            #new grocery
            grocery = GroceryItem(  name=body['grocery'],
                                    category='misc',
                                    quantity=-1*extractNum(body['quantity']))
        grocery.save()
    return update_lists(request)

@csrf_exempt
def remove_grocery(request):
    if(request.method == 'GET'):
        return render(request,"assistant/grocery.html")
    print(request.POST)
    if(('quantity' in request.POST) and ('grocery' in request.POST)):
        if(int(request.POST['quantity']) == 0):
            grocery = GroceryItem.objects.get(name=request.POST['grocery'])
            grocery.quantity = 0
            grocery.save()
            return update_lists(request)

    body = json.loads(request.body.decode('utf-8'))
    if(('quantity' in body) and ('grocery' in body)):
        try:
            #known grocery
            grocery = GroceryItem.objects.get(name=body['grocery'])
            quant = int(body['quantity'])
            if(grocery.quantity < 0):#in grocery list
                if(quant <= abs(grocery.quantity)):
                    grocery.quantity += quant
                else:
                    grocery.quantity = 0
                grocery.save()
        except:
            #grocery not found
            pass
    return update_lists(request)

def update_lists(request):
    json_response = []
    list_obj = {}
    for list_type in lists:
        list_type_obj={}
        for grocery in GroceryItem.objects.filter(category=list_type):
            if(grocery.quantity != 0):
                list_type_obj[grocery.name] = grocery.quantity
        if(len(list_type_obj) > 0):
            list_obj[list_type] = list_type_obj
    json_response.append(list_obj)
    response_json = json.dumps(json_response)
    response = HttpResponse(response_json, content_type='application/json')
    return response

