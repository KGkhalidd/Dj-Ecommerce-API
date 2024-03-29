from django.urls import path, include
from . import views

urlpatterns = [
    path('register', views.register , name='register'),
    path('user_info', views.user_info , name='user_info'),
    path('user_info/update', views.update_user , name='update'),
    path('forgot_password', views.forgot_password , name='forgot_password'),
    path('reset-password/<str:token>', views.reset_password , name='reset_password'),
]
