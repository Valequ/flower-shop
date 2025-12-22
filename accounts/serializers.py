from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}  
    )
    
    class Meta:
        model = CustomUser
        fields = (
            'username', 
            'email', 
            'phone', 
            'full_name', 
            'password',
            'agreed_to_terms', 
            'agreed_to_offer', 
            'agreed_to_privacy',
            'role'  
        )
        extra_kwargs = {
            'agreed_to_terms': {'required': True},
            'password': {'write_only': True},
            'role': {'read_only': True}  
        }
    
    def validate(self, attrs):
        if not attrs.get('agreed_to_terms'):
            raise serializers.ValidationError({
                "agreed_to_terms": "Необходимо согласие на обработку персональных данных"
            })
        
        if CustomUser.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({
                "email": "Пользователь с таким email уже существует"
            })
        
        if CustomUser.objects.filter(username=attrs.get('username')).exists():
            raise serializers.ValidationError({
                "username": "Пользователь с таким логином уже существует"
            })
        
        return attrs
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            full_name=validated_data.get('full_name', ''),
            agreed_to_terms=validated_data.get('agreed_to_terms', False),
            agreed_to_offer=validated_data.get('agreed_to_offer', False),
            agreed_to_privacy=validated_data.get('agreed_to_privacy', False),
            role=CustomUser.Role.USER  
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )

class UserProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = (
            'id', 
            'username', 
            'email', 
            'phone', 
            'full_name', 
            'avatar_url',
            'date_joined', 
            'last_login'
        )
        read_only_fields = ('date_joined', 'last_login', 'avatar_url')
    
    def get_avatar_url(self, obj):
        request = self.context.get('request')
        if obj.avatar and hasattr(obj.avatar, 'url'):
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None