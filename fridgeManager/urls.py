from django.conf.urls import url
from fridgeManager import views 
from django.contrib.auth.views import LoginView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sign-up$', views.sign_up, name='sign_up'),
    url(r'^sign-in/$', LoginView.as_view(template_name='fridgeManager/sign_in.html'), name='sign_in'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^my-fridge$', views.my_fridge, name="my_fridge"),
    url(r'^ajax/get-fridge$', views.get_fridge, name="get_fridge"),
    url(r'^ajax/add_new_food$', views.add_new_food_item, name="add_new_food_item"),
    url(r'^ajax/add_new_fridge_item$', views.add_new_fridge_item, name="add_new_fridge_item"),
    url(r'^ajax/add_new_category$', views.add_new_category, name="add_new_category"),
    url(r'^ajax/my_fridge_forms$', views.my_fridge_forms, name="my_fridge_forms"),
    url(r'^ajax/recipe_modal$', views.recipe_modal, name="recipe_modal"),
    url(r'^delete$', views.delete_from_fridge,name="delete_from_fridge"),
]