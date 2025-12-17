from django.contrib import admin
from django.urls import path
from django.urls import include, path

from catalog import views
app_name = 'catalog'
urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('product/', views.product, name='product'),

]
