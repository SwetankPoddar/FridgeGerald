from django.shortcuts import render, redirect
from fridgeManager.forms import new_food_item_form, UserForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    response = render(request, 'fridgeManager/index.html', context={})
    return response


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

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Account successfully created!')
            return redirect('index')
    else:
        user_form = UserForm()

    context_dict = {'user_form': user_form}
    return render(request, 'fridgeManager/sign_up.html', context_dict)


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')
