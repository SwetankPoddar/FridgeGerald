from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import os
import datetime
from django.conf import settings
from django.core.validators import RegexValidator

def get_image_path(instance, filename):
    return os.path.join('image_photos', str(instance.id), filename)

class food_category(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="The name of the category")

class food_item(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="The name of food")
    duration = models.IntegerField(help_text="How long does this item stay good for?", validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    category = models.ForeignKey(food_category, on_delete=models.SET_NULL, null = True)


class Fridge(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class FridgeFoodItem(models.Model):
    food = models.ForeignKey(food_item, on_delete=models.CASCADE)
    best_before = models.DateField(default=datetime.date.today)
    quantity = models.CharField(max_length=50)
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    def __str__(self):
        return self.user.username
