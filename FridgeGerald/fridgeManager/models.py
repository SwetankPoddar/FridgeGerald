from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import os

def get_image_path(instance, filename):
    return os.path.join('image_photos', str(instance.id), filename)

class food_category(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="The name of the category")

class food_item(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="The name of food")
    duration = models.IntegerField(help_text="How long does this item stay good for?", validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    category = models.ForeignKey(food_category, on_delete=models.SET_NULL, null = True)
