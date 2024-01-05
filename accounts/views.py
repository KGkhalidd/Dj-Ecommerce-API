from datetime import datetime, timedelta
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .serializers import SignUpSerializer, UserSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

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


def get_current_host(request):
    protocol = 'https://' if request.is_secure() else 'http://'
    host = request.get_host()
    return protocol + host + '/api' # http://  +  127.0.0.1:8000  +  /api/


@api_view(['POST'])
def forgot_password(request):
    if 'email' in request.data:
        try:
            user = User.objects.get(email=request.data['email'])
            user.profile.reset_password_token = get_random_string(length=32)
            user.profile.reset_password_expires = datetime.now() + timedelta(minutes=30)
            user.profile.save()
            send_mail(
                'Reset Password From Ecommerce App',
                f'Please click the following link to reset your password: {get_current_host(request)}/reset-password/{user.profile.reset_password_token}',
                'khaledgamal@gmail.com',
                [user.email],
                )
            return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reset_password(request, token):
    if 'password' and 'confirm_password' in request.data:
        try:
            # bring the user by the token
            user = User.objects.get(profile__reset_password_token=token)
            if user.profile.reset_password_expires.replace(tzinfo=None) > datetime.now():
                if user.check_password(request.data['password']):
                    return Response({'error': 'New password must be different from the old password'}, status=status.HTTP_400_BAD_REQUEST)
                elif request.data['password'] != request.data['confirm_password']:
                    return Response({'error': 'Password and Confirm password do not match'}, status=status.HTTP_400_BAD_REQUEST)
                user.set_password(request.data['password'])
                user.profile.reset_password_token = None
                user.profile.reset_password_expires = None
                user.profile.save()
                user.save()
                return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Password and Confirm_password are required'}, status=status.HTTP_400_BAD_REQUEST)