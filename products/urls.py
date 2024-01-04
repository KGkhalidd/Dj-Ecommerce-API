from django.urls import path, include
from . import views


urlpatterns = [
    path('products', views.product_list, name='products'),
    path('products/<int:pk>', views.product_detail, name='product-detail'),
    path('products/create', views.product_create, name='product-create'),
    path('products/<int:pk>/update', views.product_update, name='product-update'),
    path('products/<int:pk>/delete', views.product_delete, name='product-delete'),
    path('products/<int:pk>/reviews', views.review_create_or_update, name='review-create-or-update'),
    path('products/<int:pk>/reviews/delete', views.review_delete, name='review-delete'),
]
