from django.urls import path, include
from . import views

urlpatterns = [
    path('register', views.register , name='register'),
    path('user_info', views.user_info , name='user_info'),
]