from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def guest_or_user_required(view_func):
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper

def user_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Для доступа к этой странице необходимо войти в систему')
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Для доступа к этой странице необходимо войти в систему')
            return redirect('accounts:login')
        
        if not (request.user.role == 'admin' or request.user.is_staff):
            messages.error(request, 'У вас нет прав для доступа к этой странице')
            return redirect('main:home')
        
        return view_func(request, *args, **kwargs)
    return wrapper