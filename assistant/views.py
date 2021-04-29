from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse

from assistant.models import *
from assistant.forms import *

import json
# Create your views here.

#categories of lists
lists=['produce','alcohol','pantry','dairy','spices','misc']
recipe_cats=['breakfast','dinner','cocktails','ingredients']

def grocery(request):
    context={'categories': lists}
    if(request.user.is_authenticated):
        context['username'] = request.user.username
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

def cookbook(request):
    context={}
    if(request.user.is_authenticated):
        context['username'] = request.user.username
    categories={}
    for cat in recipe_cats:
        recipes_obj=[]
        recipes = RecipeItem.objects.filter(category=cat)
        for recipe in recipes:
            recipe_obj = {
                    'name': recipe.name,
                    'shortname': recipe.shortname,
                    'thumbnail': recipe.shortname}
            makeable = True
            gluten = False
            dairy = False
            missing_ingredients = []
            planned_ingredients = []
            ingredients = []
            for ingr in recipe.ingredients.all():
                ingredients.append(ingr.name)
                if(ingr.quantity == 0 and ingr.name!=' water'):
                    if(len(RecipeItem.objects.filter(name=(ingr.name[1:].lower())))>0):
                        home_ingr = RecipeItem.objects.get(name=(ingr.name[1:].lower()))
                        for home_ingr_ingr in home_ingr.ingredients.all():
                            if(home_ingr_ingr.quantity == 0 and home_ingr_ingr.name!=' water'):
                                missing_ingredients.append(ingr.name)
                                makeable = False
                                break;
                            elif(home_ingr_ingr.quantity < 1 and home_ingr_ingr.name!=' water'):
                                planned_ingredients.append(ingr.name)
                                makeable = False
                                break;
                    else:
                        missing_ingredients.append(ingr.name)
                        makeable = False
                elif(ingr.quantity < 1 and ingr.name!=' water'):
                    if(len(RecipeItem.objects.filter(name=(ingr.name[1:].lower())))>0):
                        home_ingr = RecipeItem.objects.get(name=(ingr.name[1:].lower()))
                        for home_ingr_ingr in home_ingr.ingredients.all():
                            if(home_ingr_ingr.quantity == 0 and home_ingr_ingr.name!=' water'):
                                missing_ingredients.append(ingr.name)
                                makeable = False
                                break;
                            elif(home_ingr_ingr.quantity < 1 and home_ingr_ingr.name!=' water'):
                                planned_ingredients.append(ingr.name)
                                makeable = False
                                break;
                    else:
                        planned_ingredients.append(ingr.name)
                        makeable = False

                if(ingr.gluten):
                    gluten = True
                if(ingr.dairy):
                    dairy = True
            recipe_obj['makeable'] = makeable
            recipe_obj['gluten'] = gluten
            recipe_obj['dairy'] = dairy
            recipe_obj['ingredients'] = ingredients
            recipe_obj['missing_ingredients'] = missing_ingredients
            recipe_obj['planned_ingredients'] = planned_ingredients
            optional_ingredients = []
            for ingr in recipe.optional_ingredients.all():
                optional_ingredients.append(ingr.name)
            recipe_obj['optional_ingredients'] = optional_ingredients
            recipes_obj.append(recipe_obj)
        categories[cat] = recipes_obj
    context['categories'] = categories

    if(request.method == 'GET'):
        return render(request,"assistant/cookbook.html", context)
    return render(request,"assistant/cookbook.html", context)

def edit(request):
    context={}
    if(request.user.is_authenticated):
        context['username'] = request.user.username
    context['recipes'] = RecipeItem.objects.all().order_by('name')
    context['ingredients'] = GroceryItem.objects.all().order_by('name')
    if(request.method == 'GET'):
        return render(request,"assistant/edit.html", context)
    return render(request,"assistant/edit.html", context)

@csrf_exempt
def swap_list(request):
    if(request.method == 'GET'):
        return render(request,"assistant/grocery.html")
    if(('quantity' in request.POST) and ('grocery' in request.POST)):
        grocery_name = request.POST['grocery'].replace(' - ',' ')
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
            grocery_name = body['grocery'].replace(' - ',' ')
            grocery = GroceryItem.objects.get(name=grocery_name)
            if(grocery.quantity > 0):#in stock list
                grocery.quantity += int(body['quantity'])
            else:
                grocery.quantity = int(body['quantity'])
        except:
            #new grocery
            grocery_name = body['grocery'].replace(' - ',' ')
            grocery = GroceryItem(  name=grocery_name,
                                    category='misc',
                                    quantity=extractNum(body['quantity']))
        grocery.save()
    return update_lists(request)

@csrf_exempt
def add_single_stock(request):
    if(request.method == 'GET'):
        return render(request,"assistant/grocery.html")
    body = json.loads(request.body.decode('utf-8'))
    for word in body:
        word = word.replace(' ','')
    if('grocery' in body):
        try:
            #known grocery
            grocery_name = body['grocery'].replace(' - ',' ')
            grocery = GroceryItem.objects.get(name=grocery_name)
            if(grocery.quantity > 0):#in stock list
                grocery.quantity += grocery.default_quant)
            else:
                grocery.quantity = grocery.default_quant)
        except:
            #new grocery
            grocery_name = body['grocery'].replace(' - ',' ')
            grocery = GroceryItem(  name=grocery_name,
                                    category='misc',
                                    quantity=1)
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
            grocery_name = body['grocery'].replace(' - ',' ')
            grocery = GroceryItem.objects.get(name=grocery_name)
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
            grocery_name = body['grocery'].replace(' - ',' ')
            grocery = GroceryItem.objects.get(name=grocery_name)
            if(grocery.quantity < 0):#in grocery list
                grocery.quantity -= int(body['quantity'])
            else:#remove from stock and add to grocery list
                grocery.quantity = -1*int(body['quantity'])
        except:
            #new grocery
            grocery_name = body['grocery'].replace(' - ',' ')
            grocery = GroceryItem(  name=grocery_name,
                                    category='misc',
                                    quantity=-1*extractNum(body['quantity']))
        grocery.save()
    return update_lists(request)

@csrf_exempt
def add_single_grocery(request):
    if(request.method == 'GET'):
        return render(request,"assistant/grocery.html")
    body = json.loads(request.body.decode('utf-8'))
    print(body)
    if('grocery' in body):
        try:
            #known grocery
            grocery_name = body['grocery'].replace(' - ',' ')
            grocery = GroceryItem.objects.get(name=grocery_name)
            if(grocery.quantity < 0):#in grocery list
                grocery.quantity -= grocery.default_quant
            else:#remove from stock and add to grocery list
                grocery.quantity = -1*grocery.default_quant
        except:
            #new grocery
            grocery_name = body['grocery'].replace(' - ',' ')
            grocery = GroceryItem(  name=grocery_name,
                                    category='misc',
                                    quantity=-1)
        grocery.save()
    return update_lists(request)

@csrf_exempt
def remove_grocery(request):
    if(request.method == 'GET'):
        return render(request,"assistant/grocery.html")
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
            grocery_name = body['grocery'].replace(' - ',' ')
            grocery = GroceryItem.objects.get(name=grocery_name)
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

def admin_login(request):
    context={}
    if(request.user.is_authenticated):
        context['username'] = request.user.username
    if(request.method == 'GET'):
        context['form'] = LoginForm()
        return render(request,'assistant/login.html', context)
    form = LoginForm(request.POST)
    context['form'] = form
    return render(request,'assistant/login.html', context)

def login_action(request):
    context={}
    if(request.user.is_authenticated):
        context['username'] = request.user.username
    if(request.method == 'GET'):
        context['form'] = LoginForm()
        return render(request,'assistant/login.html',context)
    form = LoginForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request,'assistant/login.html',context)
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    login(request,new_user)
    return redirect(reverse('cookbook'))

def select_recipe(request):
    json_response = []
    list_obj = {}
    if('recipe' in request.POST):
        recipe = RecipeItem.objects.get(shortname=request.POST['recipe'])
        list_obj['name'] = recipe.name
        list_obj['shortname'] = recipe.shortname
        list_obj['category'] = recipe.category
        ingredients = []
        for ingredient in recipe.ingredients.all():
            ingredients.append(ingredient.name)
        list_obj['ingredients'] = ingredients
        options = []
        for option in recipe.optional_ingredients.all():
            options.append(option.name)
        list_obj['options'] = options
    json_response.append(list_obj)
    response_json = json.dumps(json_response)
    response = HttpResponse(response_json, content_type='application/json')
    return response

def select_ingredient(request):
    json_response = []
    list_obj = {}
    if('ingredient' in request.POST):
        ingredient = GroceryItem.objects.get(name=request.POST['ingredient'])
        list_obj['name'] = ingredient.name
        list_obj['category'] = ingredient.category
        list_obj['gluten'] = ingredient.gluten
        list_obj['dairy'] = ingredient.dairy
        list_obj['default_quant'] = ingredient.default_quant
        list_obj['units'] = ingredient.units
    json_response.append(list_obj)
    response_json = json.dumps(json_response)
    response = HttpResponse(response_json, content_type='application/json')
    return response

def edit_recipe(request):
    context = {}
    if(request.method == 'GET'):
        return render(request,"assistant/edit.html", context)
    if('recipe_shortname' in request.POST):
        shortname = request.POST['recipe_shortname']
    else:
        return render(request,"assistant/edit.html", context)
    if('recipe_name' in request.POST):
        name = request.POST['recipe_name']
    if('recipe_cat' in request.POST):
        category = request.POST['recipe_cat'].lower()
    if(len(RecipeItem.objects.filter(shortname=shortname)) > 0):
        recipe = RecipeItem.objects.get(shortname=shortname)
        if(recipe.name != name):
            recipe.name = name
        if(recipe.category != category):
            recipe.category = category
    else:
        recipe = RecipeItem(name=name, shortname=shortname, category=category)
        recipe.save()
    curIngr={}
    curOpt={}
    for ingredient in recipe.ingredients.all():
        curIngr[ingredient.name] = False
    for option in recipe.optional_ingredients.all():
        curOpt[option.name] = False
    #add ingredients found in post
    if('num_ingredients' in request.POST):
        num_ingredients = int(request.POST['num_ingredients'])
        for i in range(num_ingredients):
            print('ingredient_input_'+str(i))
            if('ingredient_input_'+str(i) in request.POST):
                ingredient_name = request.POST['ingredient_input_'+str(i)]
                if(ingredient_name[0] != ' '):
                    ingredient_name = ' '+ingredient_name
                ingredient_name = ingredient_name.replace('+',' ').lower()
                if(ingredient_name in curIngr):
                    curIngr[ingredient_name] = True
                if(len(GroceryItem.objects.filter(name=ingredient_name)) > 0):
                    ingredient = GroceryItem.objects.get(name=ingredient_name)
                else:
                    ingredient = GroceryItem(name=ingredient_name, quantity=0, category='misc')
                    ingredient.save()
                if(ingredient not in recipe.ingredients.all()):
                    recipe.ingredients.add(ingredient)
    if('num_options' in request.POST):
        num_options = int(request.POST['num_options'])
        for i in range(num_options):
            if('option_input_'+str(i) in request.POST):
                option_name = request.POST['option_input_'+str(i)]
                if(option_name[0] != ' '):
                    option_name = ' '+option_name
                option_name = option_name.replace('+',' ').lower()
                if(option_name in curOpt):
                    curOpt[option_name] = True
                if(len(GroceryItem.objects.filter(name=option_name)) > 0):
                    option = GroceryItem.objects.get(name=option_name)
                else:
                    option = GroceryItem(name=option_name, quantity=0, category='misc')
                    option.save()
                if(option not in recipe.optional_ingredients.all()):
                    recipe.optional_ingredients.add(option)
    #remove ingredients not found in post
    for ingrName,included in curIngr.items():
        ingredient = GroceryItem.objects.get(name=ingrName)
        if(not included):
            recipe.ingredients.remove(ingredient)
    for ingrName,included in curOpt.items():
        ingredient = GroceryItem.objects.get(name=ingrName)
        if(not included):
            recipe.optional_ingredients.remove(ingredient)
    recipe.save()
    return edit(request)

def edit_ingredient(request):
    context = {}
    if(request.method == 'GET'):
        return render(request,"assistant/edit.html", context)
    if('ingredient_name' in request.POST):
        name = ' '+request.POST['ingredient_name'].lower()
    if('ingr_cat' in request.POST):
        category = request.POST['ingr_cat'].lower()
    gluten = False
    if('ingredient_gluten' in request.POST):
        if(request.POST['ingredient_gluten'] == 'on'):
            gluten = True
    dairy = False
    if('ingredient_dairy' in request.POST):
        if(request.POST['ingredient_dairy'] == 'on'):
            dairy = True
    if('ingredient_default_quant' in request.POST):
        default_quant = request.POST['ingredient_default_quant']
    if('ingredient_units' in request.POST):
        units = request.POST['ingredient_units']
    if(len(GroceryItem.objects.filter(name=name)) > 0):
        ingr = GroceryItem.objects.get(name=name)
        if(ingr.category != category):
            ingr.category = category
        if(ingr.gluten != gluten):
            ingr.gluten = gluten
        if(ingr.dairy != dairy):
            ingr.dairy = dairy
        if(ingr.default_quant != default_quant):
            ingr.default_quant = default_quant
        if(ingr.units != units):
            ingr.units = units
    else:
        ingr = GroceryItem(name=name,
                            category=category,
                            gluten=gluten,
                            dairy=dairy,
                            default_quant=default_quant,
                            units=units)
    ingr.save()
    return edit(request)

@csrf_exempt
def buy_recipe(request):
    context = {}
    if(request.method == 'GET'):
        return render(request,"assistant/cookbook.html", context)
    if('recipe' in request.POST):
        recipe = RecipeItem.objects.get(shortname=request.POST['recipe'])
    for ingr in recipe.ingredients.all():
        if(ingr.quantity == 0 and ingr.name!=' water'):
            if(len(RecipeItem.objects.filter(name=(ingr.name[1:].lower())))>0):
                home_ingr = RecipeItem.objects.get(name=(ingr.name[1:].lower()))
                for home_ingr_ingr in home_ingr.ingredients.all():
                    if(home_ingr_ingr.quantity == 0 and home_ingr_ingr.name!=' water'):
                        ingr.quantity = ingr.default_quant*-1
                        ingr.save()
                        break;
            else:
                ingr.quantity = ingr.default_quant*-1
                ingr.save()

    for i in range(len(ingr.optional_ingredients.all())):
        if('optional'+str(i) in request.POST):
            ingr = recipe.optional_ingredients.get(name=(request.POST['optional'+str(i)].replace('_',' ')))
            if(ingr.quantity == 0 and ingr.name != 'water'):
                if(len(RecipeItem.objects.filter(name=(ingr.name[1:].lower())))>0):
                    home_ingr = RecipeItem.objects.get(name=(ingr.name[1:].lower()))
                    for home_ingr_ingr in home_ingr.ingredients.all():
                        if(home_ingr_ingr.quantity == 0 and home_ingr_ingr.name!=' water'):
                            ingr.quantity = ingr.default_quant*-1
                            ingr.save()
                            break;
                else:
                    ingr.quantity = ingr.default_quant*-1
                    ingr.save()
    response_json = json.dumps([])
    response = HttpResponse(response_json, content_type='application/json')
    return response
