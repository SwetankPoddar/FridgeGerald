from django.contrib import admin
from fridgeManager.models import FridgeFoodItem, Fridge, food_category, food_item

admin.site.register(Fridge)

admin.site.register(FridgeFoodItem)

admin.site.register(food_category)

admin.site.register(food_item)