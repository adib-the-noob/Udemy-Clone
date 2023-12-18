from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
            'email',
            'password',
            'phone_number',
            'profile_picture',
        ]
        
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def validate(self, data):
        email = data['email']
        full_name = data['full_name']
        
        if full_name is None:
            raise serializers.ValidationError('Full name is required')
        
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise serializers.ValidationError('This email has already been registered')
        return data
    
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long')
        return value
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        email = data['email']
        password = data['password']
        
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            user = user_qs.first()
            if not user.check_password(password):
                raise serializers.ValidationError('Incorrect password')
        else:
            raise serializers.ValidationError('This email has not been registered')
        return data