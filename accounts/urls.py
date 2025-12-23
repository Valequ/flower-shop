from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    profile, login, register, edit_profile_page,
    LoginAPIView, RegisterAPIView, ProfileAPIView, LogoutAPIView,
    add_to_cart, remove_from_cart, update_cart_item, create_order  )
from accounts import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'accounts'

urlpatterns = [
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile_page, name='edit_profile'),
    path('register/', register, name='register'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path('logout/', views.logout_view, name='logout'),
    path('download-data/', views.download_user_data, name='download_data'),

    path('add-to-cart/<slug:product_slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('create-order/', views.create_order, name='create_order'),

    path('api/login/', LoginAPIView.as_view(), name='login_api'),
    path('api/register/', RegisterAPIView.as_view(), name='register_api'),
    path('api/logout/', LogoutAPIView.as_view(), name='logout_api'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', ProfileAPIView.as_view(), name='profile_api'),
    path('api/profile/update/', ProfileAPIView.as_view(), name='update_profile_api'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)