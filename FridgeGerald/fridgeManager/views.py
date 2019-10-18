from django.shortcuts import render

def index(request):
    response = render(request, 'fridgeManager/index.html', context={})
    return response
