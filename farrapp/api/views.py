from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .serializers import UserSerializer

from .models import Ej_establishment, Trie, Node_establishment
from .search import search

@api_view(['GET'])
def add_est (request):
    name = request.GET['name']
    new_establishment = Ej_establishment(name=name)
    new_establishment.save()
    return Response(f"added", status=status.HTTP_200_OK)

@api_view(['GET'])
def search_query (request):
    name = request.GET['name']
    search(name)
    return Response(f"okis", status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({'error': 'Wrong password'}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({'token': token.key, "username": serializer.data["username"]}, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, "username": serializer.data["username"]}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test(request):
    return Response(f"auth OK for user {request.user.username}", status=status.HTTP_200_OK)
