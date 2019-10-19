from django.shortcuts import render, redirect
from fridgeManager.forms import new_food_item_form, UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from fridgeManager.models import Fridge, FridgeFoodItem
from datetime import datetime


def index(request):
    response = render(request, 'fridgeManager/index.html', context={})
    return response


@login_required
def my_fridge(request):
    context = {
        'content': [
           # 'addToFridge': addToFridgeForm,
           # 'addCategory': addCategoryForm,
           # 'addFoodItem': new_food_item_form,
            ]
    }
    response = render(request, 'fridgeManager/my_fridge.html', context=context)
    return response

@login_required
def delete_from_fridge(request):
    try:
        #FridgeFoodItem.
        pass
    except FridgeFoodItem.DoesNotExist:
        messages.warning(request, 'Incorrect item!')

    redirect(reverse("my_fridge"))

@login_required
def get_fridge(request):
    items = []
    for item in request.user.fridge.fridgefooditem_set.all():
        days = (item.best_before - datetime.now()).days
        items.append({
            'name': item.food.name,
            'category': item.food.category.name,
            'quantity': item.quantity,
            'best_before': days
        })

    items = [
        {
            'id': 5,
            'name': 'Apple',
            'category': 'Fruit',
            'quantity': '5',
            'best_before': '6'
        },
        {
            'id': 5,
            'name': 'Pear',
            'category': 'Fruit',
            'quantity': '2',
            'best_before': '3'
        },
        {
            'id': 5,
            'name': 'Cucumber',
            'category': 'Vegetable',
            'quantity': '1',
            'best_before': '8'
        },
        {
            'id': 5,
            'name': 'Chicken Breasts',
            'category': 'Meat',
            'quantity': '500g',
            'best_before': '1'
        },
        {
            'id': 5,
            'name': 'Rice',
            'category': 'Other',
            'quantity': '500g',
            'best_before': '54'
        }
    ]
    return JsonResponse(items, safe=False)


def add_new_item(request):
    
    newRequest = new_food_item_form(request.POST or None)

    if(request.method == "POST"):
        if newRequest.is_valid():
            newRequest = newRequest.save()
            return redirect(reverse("index"))
    
    newRequest.action = str(reverse('add_new_item'))
    newRequest.formFor = 'Add a new item to fridge'
    return render(request, 'fridgeManager/form.html', context={'form': newRequest})


def sign_up(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            fridge = Fridge(user=user)
            fridge.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Account successfully created!')
            return redirect('index')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'fridgeManager/sign_up.html', context_dict)


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')
