from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .Conejito_Auth import CustomToken, TokenAuthentication
from .models import ClientModel, EstablishmentModel, Rating
from .serializers import UserSerializer, EstablishmentSerializer, EstablishmentQuerySerializer, UserUpdateInfoSerializer, EstablishmentUpdateInfoSerializer

from .search import search

from django.core.exceptions import ObjectDoesNotExist

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search_query (request):
    name = request.GET['name']
    matched_establishments = search(name)
    query_set = []
    for i in matched_establishments:
        query_set.append(EstablishmentModel.objects.get(pk = i))
    serializer = EstablishmentQuerySerializer(query_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    user_type = request.data.get('user_type', None)
    if user_type is None:
        return Response({'error': 'You must provide a user type'}, status=status.HTTP_404_NOT_FOUND)
    if user_type == 'client':
        user = get_object_or_404(ClientModel, username=request.data['username'])
        serializer = UserSerializer(instance=user)
    elif user_type == 'establishment':
        user = get_object_or_404(EstablishmentModel, username=request.data['username'])
        serializer = EstablishmentSerializer(instance=user)
    else:
        return Response({'error': 'User type not found'}, status=status.HTTP_404_NOT_FOUND)
    if not user.check_password(request.data['password']):
        return Response({'error': 'Wrong password'}, status=status.HTTP_404_NOT_FOUND)
    token, created = CustomToken.objects.get_or_create(user=user)
    return Response({'token': token.key, "username": serializer.data["username"]}, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup(request):
    user_type = request.data.get('user_type', None)
    if user_type is None:
        return Response({'error': 'You must provide a user type'}, status=status.HTTP_404_NOT_FOUND)
    if user_type == 'client':
        serializer = UserSerializer(data=request.data)
    elif user_type == 'establishment':
        serializer = EstablishmentSerializer(data=request.data)
    else:
        return Response({'error': 'User type not found'}, status=status.HTTP_404_NOT_FOUND)

    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        token = CustomToken.objects.create(user=user)
        return Response({'token': token.key, "username": serializer.data["username"]}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_auth(request):
    return Response(f"auth OK for user {request.user.username}", status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def establishments_list(request):
    queryset = EstablishmentModel.objects.all()
    serializer = EstablishmentQuerySerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def filter_sort(request):
    queryset = EstablishmentModel.objects.all()
    serializer = EstablishmentQuerySerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def rate(request):
    client_r = ClientModel.objects.get(username = request.user.username)
    establishment_r = EstablishmentModel.objects.get(pk = request.data.get('establishment_id'))
    stars = request.data.get('rating')
    try:
        cur_rate = Rating.objects.get(client = client_r, establishment = establishment_r)
        establishment_r.overall_rating += stars - cur_rate.stars            
        cur_rate.stars = stars
        establishment_r.save()
        cur_rate.save()
    except ObjectDoesNotExist:
        Rating.objects.create(stars = stars, client = client_r, establishment = establishment_r)
        establishment_r.overall_rating += stars
        establishment_r.number_of_reviews += 1
        establishment_r.save()
    return Response({'user' : request.user.username, 'establishment' : establishment_r.name}, status=status.HTTP_202_ACCEPTED)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_preferences(request):
    user_type = request.data.get('user_type', None)
    
    if user_type is None:
        return Response({'error': 'You must provide a user type'}, status=status.HTTP_404_NOT_FOUND)
    if user_type == 'client':
        obj = get_object_or_404(ClientModel, username=request.user.username)
        #print (obj)
        serializer = UserUpdateInfoSerializer(obj, data=request.data)
        
    elif user_type == 'establishment':
        obj = get_object_or_404(EstablishmentModel, username=request.user.username)
        serializer = EstablishmentUpdateInfoSerializer(obj, data=request.data)
    else:
        return Response({'error': 'User type not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if serializer.is_valid():
        user = serializer.save()
        user.save()

        return Response(f"Update accepted for user {request.user.username}", status=status.HTTP_202_ACCEPTED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user_type = request.data.get('user_type', None)
    
    if user_type is None:
        return Response({'error': 'You must provide a user type'}, status=status.HTTP_404_NOT_FOUND)
    if user_type == 'client':
        obj = ClientModel.objects.get(username=request.user.username)
        ClientModel.delete(obj)
    elif user_type == 'establishment':
        obj = EstablishmentModel.objects.get(username=request.user.username)
        EstablishmentModel.delete(obj)
    else:
        return Response({'error': 'User type not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(f"Delete accepted for user {request.user.username}", status=status.HTTP_202_ACCEPTED)
    
