import os
from tokenize import TokenError
from django.shortcuts import render,redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login as django_login, logout as django_logout 

from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
# Create your views here.

from rest_framework.parsers import MultiPartParser, FormParser

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AvatarUploadForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import CartItem, Order, OrderItem
from catalog.models import Product
from django.http import HttpResponse
import json
from datetime import datetime


@login_required
def upload_avatar(request):
    if request.method == 'POST':
        if request.user.avatar and 'avatars/default' not in request.user.avatar.name:
            old_avatar_path = request.user.avatar.path
            if os.path.exists(old_avatar_path):
                os.remove(old_avatar_path)
        
        form = AvatarUploadForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аватар успешно обновлен!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Ошибка при загрузке файла')
    
    return redirect('accounts:edit_profile')

    
@login_required
def profile(request):
    cart_items = CartItem.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    total_price = sum(item.total_price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'cart_total_price': total_price,
        'cart_item_count': cart_items.count(),
        'orders': orders,
    }
    
    return render(request, 'accounts/profile.html', context)
def login(requset):
    return render (requset,'accounts/login.html')
def register(requset):
    return render (requset,'accounts/register.html')
def edit_profile_page(request):
    return render(request, 'accounts/edit_profile.html')

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            if user:
                django_login(request, user)
                
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': UserProfileSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'message': 'Вход выполнен успешно'
                })
            return Response(
                {'error': 'Неверный логин или пароль'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = UserProfileSerializer(
            request.user, 
            data=request.data, 
            partial=True  
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Профиль успешно обновлен',
                'user': serializer.data
            })
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserProfileSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Регистрация успешна! Добро пожаловать в наш магазин цветов!'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'errors': serializer.errors,
            'message': 'Ошибка регистрации. Проверьте введенные данные.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                except TokenError:
                    pass
            
            django_logout(request)
            
            return Response({
                "success": True,
                "message": "Выход выполнен успешно"
            })
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Ошибка при выходе: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
        
def logout_view(request):
    django_logout(request)
    
    return redirect('accounts:login')


# корзина
@login_required
def add_to_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'Товар "{product.name}" добавлен в корзину!')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': CartItem.objects.filter(user=request.user).count()
        })
    
    return redirect('catalog:product', slug=product_slug)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    
    return redirect('accounts:profile')

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    
    action = request.GET.get('action')
    
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            return redirect('accounts:profile')
    
    return redirect('accounts:profile')


@login_required
def create_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items:
        messages.error(request, 'Ваша корзина пуста!')
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address')
        payment_method = request.POST.get('payment_method')
        
        if not delivery_address:
            messages.error(request, 'Пожалуйста, укажите адрес доставки!')
            return redirect('accounts:profile')
        
        if not payment_method:
            messages.error(request, 'Пожалуйста, выберите способ оплаты!')
            return redirect('accounts:profile')
        
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        import random
        order_number = f"ORD{random.randint(1000000, 9999999)}"

        order = Order.objects.create(
            user=request.user,
            order_number=order_number, 
            total_price=total_price,
            delivery_address=delivery_address,
            payment_method=payment_method,
            status='new'
        )
        
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price  
            )
        
        cart_items.delete()
        
        messages.success(request, f'Заказ #{order.order_number} успешно оформлен!')
        return redirect('accounts:profile')
    
    return redirect('accounts:profile')


@login_required
def download_user_data(request):
    user = request.user
    
    user_data = {
        "personal_info": {
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "phone": user.phone,
            "date_joined": user.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": user.last_login.strftime("%Y-%m-%d %H:%M:%S") if user.last_login else None,
        },
    }
    
    json_data = json.dumps(user_data, indent=2, ensure_ascii=False)
    
    filename = f"user_data_{user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response
