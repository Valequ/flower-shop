from django.shortcuts import render

from catalog.models import Product

# Create your views here.

def home(request):
    latest_products = Product.objects.all().order_by('-created_at')[:4]
    
    context = {
        'featured_products': latest_products,
        'user': request.user, 
    }
    return render(request, 'main/home.html', context)

def catalog(request):
    return render(request, 'catalog/catalog.html')