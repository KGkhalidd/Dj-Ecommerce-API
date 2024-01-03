from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import SignUpSerializer, UserSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status

@api_view(['POST'])
def register(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        if not User.objects.filter(email = serializer.validated_data['email']).exists():
            user = User.objects.create_user(
                username=serializer.validated_data['email'],
                first_name = serializer.validated_data['first_name'],
                last_name = serializer.validated_data['last_name'],
                email = serializer.validated_data['email'],
                password = serializer.validated_data['password']
            )
            return Response({'message': 'Account created successfully', 'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)