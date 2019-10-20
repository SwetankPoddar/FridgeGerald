from django.shortcuts import render, redirect
from fridgeManager.forms import new_food_item_form, UserForm, UserProfileForm,add_to_fridge_form,create_category_form
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
    all_forms = []
    #### New item form
    form = new_food_item_form()
    form.action = reverse("add_new_item")
    form.title = "Add a new item!"
    form.submitName = "Add a new item"
    form.modalName = "createFoodModal"
    all_forms.append(form)
    #### add a item to fridge form

    form = add_to_fridge_form()
    #form.action = reverse("add_to_fridge")
    form.title = "Add to fridge"
    form.submitName = "Add to frdige!"
    form.modalName = "addFoodToFridgeModal"

    all_forms.append(form)
    #### New category form

    form = create_category_form()
    #form.action = reverse("create_new_category")
    form.title = "Create new category"
    form.submitName = "Create new category!"
    form.modalName = "createCategoryModal"

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


def add_new_item(request):
    
    newRequest = new_food_item_form(request.POST or None)

    if(request.method == "POST"):
        if newRequest.is_valid():
            newRequest = newRequest.save()
    
    return reverse("my_fridge")



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
