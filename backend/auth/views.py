from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer
import jwt
from django.conf import settings
from datetime import datetime, timedelta

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(email=email, password=password)
        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate JWT token
        token = jwt.encode(
            {
                'user_id': str(user.id),
                'exp': datetime.utcnow() + timedelta(days=1)
            },
            settings.JWT_SECRET_KEY,
            algorithm='HS256'
        )
        
        return Response({
            'token': token,
            'user': UserSerializer(user).data
        })
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT token
            token = jwt.encode(
                {
                    'user_id': str(user.id),
                    'exp': datetime.utcnow() + timedelta(days=1)
                },
                settings.JWT_SECRET_KEY,
                algorithm='HS256'
            )
            
            return Response({
                'token': token,
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 