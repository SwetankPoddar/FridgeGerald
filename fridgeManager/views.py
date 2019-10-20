from django.shortcuts import render, redirect
from fridgeManager.forms import new_food_item_form, UserForm, UserProfileForm, new_fridge_item_form, new_category_form
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from fridgeManager.models import Fridge, FridgeFoodItem
from fridgeManager.control import get_recipes
from datetime import datetime


def index(request):
    response = render(request, 'fridgeManager/index.html', context={})
    return response


@login_required
def my_fridge(request):
    #top_foods = request.user.fridge.fridgefooditem_set.all().order_by('-best_before')[:5]
    top_foods = ['tomato', 'potato', 'ketchup','chicken']
    all_forms = get_my_fridge_forms()

    context = {
        'all_forms': all_forms,
        'recipes': get_recipes(top_foods)
    }
    response = render(request, 'fridgeManager/my_fridge.html', context=context)
    return response

@login_required
def delete_from_fridge(request):
    try:
        fridge = request.user.fridge
        fridgeItem = FridgeFoodItem.objects.get(fridge = fridge, id = request.GET['id'])
        fridgeItem.delete()
        messages.success(request, "Sucesfully consumed/deleted!")
    except FridgeFoodItem.DoesNotExist:
        messages.warning(request, 'Incorrect item!')
    finally:
        return redirect(reverse("my_fridge"))

@login_required
def get_fridge(request):
    items = []
    for item in request.user.fridge.fridgefooditem_set.all():
        days = (item.best_before - datetime.now().date()).days
        items.append({
            'id':item.id,
            'name': item.food.name,
            'category': item.food.category.name,
            'quantity': item.quantity,
            'best_before': days
        })
    return JsonResponse(items, safe=False)


def add_new_food_item(request):
    newRequest = new_food_item_form(request.POST or None)

    if(request.method == "POST"):
        if newRequest.is_valid():
            newRequest = newRequest.save()
    
    return JsonResponse({'status': 'success'})


def add_new_fridge_item(request):
    newRequest = new_fridge_item_form(request.POST or None)

    if(request.method == "POST"):
        if newRequest.is_valid():
            newRequest = newRequest.save(commit=False)
            newRequest.fridge = request.user.fridge
            newRequest.save()
    
    return JsonResponse({'status': 'success'})


def add_new_category(request):
    newRequest = new_category_form(request.POST or None)

    if(request.method == "POST"):
        if newRequest.is_valid():
            newRequest = newRequest.save()
    
    return JsonResponse({'status': 'success'})


def get_my_fridge_forms():
    all_forms = []
    #### New item form
    form = new_food_item_form()
    form.action = reverse("add_new_food_item")
    form.title = "Add a new food!"
    form.submitName = "Add a new food"
    form.id = "new_food"

    all_forms.append(form)
    #### add a item to fridge form
    form = new_fridge_item_form()
    form.action = reverse("add_new_fridge_item")
    form.title = "Add a new item!"
    form.submitName = "Add a new item"
    form.id = "new_item"

    all_forms.append(form)


    #### New category form
    form = new_category_form()
    form.action = reverse("add_new_category")
    form.title = "Add a new category!"
    form.submitName = "Add a new category"
    form.id = "new_category"

    all_forms.append(form)
    return all_forms


def my_fridge_forms(request):
    all_forms = get_my_fridge_forms()
    context = {
        'all_forms': all_forms
    }
    response = render(request, 'fridgeManager/my_fridge_forms.html', context=context)
    return response



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
