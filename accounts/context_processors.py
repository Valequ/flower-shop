from .models import CartItem

def cart_context(request):
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
        return {'cart_item_count': cart_count}
    return {'cart_item_count': 0}