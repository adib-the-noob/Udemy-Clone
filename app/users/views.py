import random
from django.core.cache import cache

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from . models import User 
from . serializers import (
    UserRegisterSerializer,
    UserLoginSerializer
)

@api_view(['POST'])
def user_registration(request):
    try:
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            otp_obj = random.randint(100000, 999999)
            cache.set(f"otp:{serializer.data['id']}", otp_obj, timeout=180)
            print(otp_obj)
            return Response({
                'message': 'Registration successful, please Verify with OTP!',
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def user_login(request):
    try:
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                'message': 'Login successful',
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
def user_otp_verification(request):
    try:
        email = request.data['email']
        otp = request.data['otp']
        
        user_obj = User.objects.get(email=email)
        
        if cache.get(f"otp:{user_obj.id}") == int(otp):
            return Response({
                'message': 'OTP verified successfully',
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'OTP verification failed',
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        