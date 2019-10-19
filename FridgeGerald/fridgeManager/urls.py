from django.conf.urls import url
from fridgeManager import views 
from django.contrib.auth.views import LoginView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sign-up$', views.sign_up, name='sign_up'),
    url(r'^sign-in/$', LoginView.as_view(template_name='fridgeManager/sign_in.html'), name='sign_in'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^add_new_item$', views.add_new_item, name="add_new_item"),
]