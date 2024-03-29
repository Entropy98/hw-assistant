from django.db import models

class GroceryItem(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    category = models.CharField(max_length=50)
    gluten = models.BooleanField(default=False)
    dairy = models.BooleanField(default=False)
    default_quant = models.IntegerField(default=1)
    units = models.CharField(default='',max_length=10)

class IngredientItem(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    units = models.CharField(default='',max_length=10)

class RecipeItem(models.Model):
    name = models.CharField(max_length=50)
    shortname = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    ingredients = models.ManyToManyField(GroceryItem,related_name='ingredients')
    ingr_quants = models.ManyToManyField(IngredientItem,related_name='ingr_quants')
    optional_ingredients = models.ManyToManyField(GroceryItem,related_name='optional_ingredients')
    instructions = models.CharField(max_length=500)
