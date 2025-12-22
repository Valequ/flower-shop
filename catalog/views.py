from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from accounts.decorators import guest_or_user_required, user_required
from .models import Category, Product
from django.contrib.auth.decorators import login_required
from django.db.models import Q




@guest_or_user_required
def catalog(request):
    categories = Category.objects.all().order_by('order')
    products = Product.objects.all().order_by('-created_at')
    
    category_slug = request.GET.get('category')
    current_category = None
    if category_slug:
        products = products.filter(category__slug=category_slug)
        current_category = category_slug
    
    search_query = request.GET.get('q')
    if search_query:
        word_replacements = {
            'ые': 'ый', 'ые': 'ой', 
            'ые': 'ая', 'ые': 'ое',
            'и': '', 'ы': '', 'ам': '', 'ами': '', 'ах': '', 
            'ов': '', 'ев': '', 'ей': '',
            'ям': '', 'ями': '', 'ях': '',
            'ом': '', 'ем': '', 'ой': '', 'ей': '',
            'у': '', 'ю': '', 'а': '', 'я': '', 'о': '', 'е': '',
        }
        
        search_words = search_query.split()
        processed_words = []
        
        for word in search_words:
            word_lower = word.lower()
            
            variants = {word_lower}
            
            for ending, replacement in word_replacements.items():
                if word_lower.endswith(ending):
                    variants.add(word_lower[:-len(ending)] + replacement)
            
            if len(word_lower) > 4:
                variants.add(word_lower[:-1])  
                variants.add(word_lower[:-2])  
            
            processed_words.append(variants)
        
        q_objects = Q()
        for word_set in processed_words:
            for word_variant in word_set:
                q_objects |= Q(name__icontains=word_variant) | Q(description__icontains=word_variant)
        
        products = products.filter(q_objects).distinct()
    
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price and min_price.isdigit():
        products = products.filter(price__gte=int(min_price))
    
    if max_price and max_price.isdigit():
        products = products.filter(price__lte=int(max_price))
    
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    
    context = {
        'categories': categories,
        'products': products_page,
        'current_category': current_category,
        'user': request.user,  
    }
    return render(request, 'catalog/catalog.html', context)

@login_required
def product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    context = {
        'product': product,
        'user': request.user,
    }
    return render(request, 'catalog/product.html', context)


