from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<slug:username>/pledges', views.user_pledges, name='user_pledges'),
]
