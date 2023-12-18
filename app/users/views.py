from django.contrib.auth import authenticate

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
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
            return Response({
                'message': 'Registration successful',
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