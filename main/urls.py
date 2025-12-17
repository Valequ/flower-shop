from django.contrib import admin
from django.urls import path
from django.urls import include, path

from main import views
app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    
]
