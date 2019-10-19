from django.shortcuts import render
from fridgeManager.forms import new_food_item_form
def index(request):
    response = render(request, 'fridgeManager/index.html', context={})
    return response


def add_new_item(request):
    
    newRequest = new_food_item_form(request.POST or None, request = request)

    if(request.method == "POST"):
        if newRequest.is_valid():
            newRequest = newRequest.save()
            return redirect(reverse("index"))
    
    newRequest.action = str(reverse('add_new_item'))
    newRequest.formFor = 'Add a new item to fridge'
    return render(request, 'fridgeManager/form.html', context={'form': newRequest})