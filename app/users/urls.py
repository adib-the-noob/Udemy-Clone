from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_registration, name='user_registration'),
    path('login/', views.user_login, name='user_login'),
    path('verify/', views.user_otp_verification, name='user_otp_verification'),
]
