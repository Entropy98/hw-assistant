from django.db import models

class GroceryItem(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    category = models.CharField(max_length=50)
    gluten = models.BooleanField(default=False)
    dairy = models.BooleanField(default=False)

class RecipeItem(models.Model):
    name = models.CharField(max_length=50)
    shortname = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    ingredients = models.ManyToManyField(GroceryItem,related_name='ingredients')
    optional_ingredients = models.ManyToManyField(GroceryItem,related_name='optional_ingredients')
    instructions = models.CharField(max_length=500)

