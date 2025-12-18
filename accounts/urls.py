from django.contrib import admin
from django.urls import path
from django.urls import include, path

from accounts import views
app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
