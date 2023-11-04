from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, EstablishmentSerializer
from .Conejito_Auth import CustomToken, TokenAuthentication
from .models import ClientModel, Establishment


@api_view(['POST'])
def login(request):
    user_type = request.data['user_type']
    if user_type == 'client':
        user = get_object_or_404(ClientModel, username=request.data['username'])
    elif user_type == 'establishment':
        user = get_object_or_404(Establishment, username=request.data['username'])
    else:
        return Response({'error': 'User type not found'}, status=status.HTTP_404_NOT_FOUND)

    if not user.check_password(request.data['password']):
        return Response({'error': 'Wrong password'}, status=status.HTTP_404_NOT_FOUND)
    token, created = CustomToken.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({'token': token.key, "username": serializer.data["username"]}, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        token = CustomToken.objects.create(user=user)
        return Response({'token': token.key, "username": serializer.data["username"]}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def signup_Establishment(request):
    serializer = EstablishmentSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        token = CustomToken.objects.create(user=user)
        return Response({'token': token.key, "username": serializer.data["username"]}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test(request):
    return Response(f"auth OK for user {request.user.username}", status=status.HTTP_200_OK)
