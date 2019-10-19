from django.conf.urls import url
from fridgeManager import views 

urlpatterns = [
    url('/', views.add_new_item, name='index'),
    url('/add_new_item/', views.add_new_item, name="add_new_item"),
]