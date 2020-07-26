from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<slug:username>/pledges', views.pledges, name='pledges'),
]
