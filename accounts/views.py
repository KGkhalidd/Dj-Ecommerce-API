from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .serializers import SignUpSerializer, UserSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def register(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        if not User.objects.filter(email = serializer.validated_data['email']).exists():
            user = User.objects.create_user(
                username=serializer.validated_data['email'].split('@')[0],
                first_name = serializer.validated_data['first_name'],
                last_name = serializer.validated_data['last_name'],
                email = serializer.validated_data['email'],
                password = serializer.validated_data['password']
            )
            return Response({'message': 'Account created successfully', 'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# This endpoint returns the details of the currently authenticated user.
# It requires the user to be authenticated (must provide a valid authentication token in their request).
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

# This endpoint allows the user to update their first name, last name, and/or password.
# It requires the user to be authenticated (must provide a valid authentication token in their request).
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        if 'password' in serializer.validated_data:
            request.user.set_password(serializer.validated_data['password'])
        serializer.save()
        return Response({'message': 'User updated successfully', 'user': serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)