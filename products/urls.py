from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('products/', views.product_list, name='products'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
]
