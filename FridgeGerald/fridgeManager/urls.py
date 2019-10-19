from django.conf.urls import url
from fridgeManager import views 

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_new_item$', views.add_new_item, name="add_new_item"),
]