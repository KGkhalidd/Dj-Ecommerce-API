from django.urls import path
from .views import OrderView

urlpatterns = [
    path('orders/', OrderView.as_view(), name='orders'),
    path('orders/<int:id>/', OrderView.as_view(), name='order-detail'),
]