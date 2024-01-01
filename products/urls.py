from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('products/', views.get_all_products, name='products'),
]
