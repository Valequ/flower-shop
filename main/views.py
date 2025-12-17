from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def catalog(request):
    return render(request, 'catalog/catalog.html')