from django.db import models

class GroceryItem(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    category = models.CharField(max_length=50)

class ListItem(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    checklist = models.ManyToManyField(GroceryItem, related_name='list', blank=True)
