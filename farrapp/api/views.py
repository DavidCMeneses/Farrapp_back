from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .Conejito_Auth import CustomToken, TokenAuthentication
from .models import ClientModel, EstablishmentModel, Rating, Category
from .serializers import UserSerializer, EstablishmentSerializer, EstablishmentQuerySerializer, UserUpdateInfoSerializer, EstablishmentUpdateInfoSerializer, EstablishmentInfoSerializer

from .search import search

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

@api_view(['POST'])
def login(request, user_type):
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

def signup(request, user_type):
    #user_type = request.data.get('user_type', None)
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
def search (request, page):
    name = request.GET['query']
    music = list(request.GET['filter_music'].split('|'))
    type_est = list(request.GET['establishment_filter'].split('|'))
    flag = request.GET['flag']

    if page == 1:
        if flag == True:
            music=[]
            type_est=[]
            client_r = ClientModel.objects.get(username = request.user.username)
            for category in client_r.categories.all():
                if category.type == 'M':
                    music.append(category.name)
                if category.type == 'E':
                    type_est.append(category.name)

        #if music or type_est is not especified take all objects
        if len(music) == 0:
            for i in Category.objects.all():
                if i.type == 'M':
                    music.append(i.name)
        if len(type_est) == 0:
            for i in Category.objects.all():
                if i.type == 'E':
                    type_est.append(i.name)

        print(music)
        print(type_est)

        query_set = []
        if len(name) > 0:
            matched_establishments = search(name)
            for i in matched_establishments:
                query_set.append(EstablishmentModel.objects.get(pk = i))
        else:
            query_set = EstablishmentModel.objects.all()
        
        match_establishment_category = [dict(), dict()]

        for i in music:
            establishment_music_i = query_set.filter(categories__name = i)
            for establishment in establishment_music_i:
                if len(match_establishment_category[0][establishment.pk]) < 1:
                    match_establishment_category[0][establishment.pk].append(i)

        for i in type_est:
            establishment_type_est_i = query_set.filter(categories__name = i)
            for establishment in establishment_type_est_i:
                if len(match_establishment_category[1][establishment.pk]) < 1:
                    match_establishment_category[1][establishment.pk].append(i)

        pagin_results = []
        for cur_establishment in query_set:
            if len(name) == 0 or len(match_establishment_category[0][cur_establishment.pk]) > 0 or len(match_establishment_category[1][cur_establishment.pk]) > 0:
                string_preferences = match_establishment_category[0][cur_establishment.pk][0] + ',' + match_establishment_category[1][cur_establishment.pk][0]
                rating = 5
                if cur_establishment.number_of_reviews > 0:
                    rating = cur_establishment.overall_rating/cur_establishment.number_of_reviews
                
                try:
                    #Authentication - without user
                    cid = "2ef223faabe64814b14d1721068497f9"
                    secret = "fcfdd55785b34f859e1e418f2c0d21ae"

                    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
                    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

                    playlist_link = cur_establishment.playlist_id
                    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
                    playlist_name = sp.playlist(playlist_id=playlist_URI, fields="name")["name"]

                except:
                    return Response({'error': 'Invalid playlist'}, status=status.HTTP_404_NOT_FOUND)

                tracks = sp.playlist_tracks(playlist_URI)["items"]
                track_name = tracks[0]["track"]["name"]
                track_id = tracks[0]["track"]["preview_url"]
                artist_name = tracks[0]["track"]["artists"][0]["name"]  
                song = {"track_name":track_name, "track_url":track_id, "artist_name":artist_name}
                pagin_results.append({"name":cur_establishment.name,
                                      "id":cur_establishment.pk,
                                      "address":cur_establishment.address,
                                      "city":cur_establishment.city,
                                      "preferences":string_preferences,
                                      "rating":rating, 
                                      "image_url":cur_establishment.image_url, 
                                      "song":song})
        
        request.session['results_search'] = list(pagin_results)
        request.session['paginator'] = Paginator(request.session['results_search'], 7)

    
    results = []
    try:
        results = request.session['paginator'].page(page)
    except PageNotAnInteger:
        return Response({'error':'page requested is not integer'},status=status.HTTP_400_BAD_REQUEST)
    except EmptyPage:
        results = request.session['paginator'].page(request.session['paginator'].num_pages)
    
    data_to_return = {'pages':request.session['paginator'].num_pages, 'results':results}
    return Response(data_to_return, status=status.HTTP_200_OK)


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
def update_preferences(request,user_type):
    #user_type = request.data.get('user_type', None)
    
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
def delete_user(request,user_type):
    #user_type = request.data.get('user_type', None)
    
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


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def fetch_establishment_info(request, establishment_id):
    establishment = EstablishmentModel.objects.get(pk = establishment_id)

    try:
        #Authentication - without user
        cid = "2ef223faabe64814b14d1721068497f9"
        secret = "fcfdd55785b34f859e1e418f2c0d21ae"

        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

        playlist_link = establishment.playlist_id
        playlist_URI = playlist_link.split("/")[-1].split("?")[0]
        playlist_name = sp.playlist(playlist_id=playlist_URI, fields="name")["name"]

    except:
        return Response({'error': 'Invalid playlist'}, status=status.HTTP_404_NOT_FOUND)

    #Json package
    serializer = EstablishmentInfoSerializer(establishment)

    #Rating
    if establishment.number_of_reviews != 0:
        rating = establishment.overall_rating/establishment.number_of_reviews
    else: 
        rating = 5

    track_list = {"playlist_name": playlist_name, "tracks":[], "rating": rating} 
    tracks = sp.playlist_tracks(playlist_URI)["items"]

    for i in range(0,min(5,len(tracks))):
        track = tracks[i]

        #Track name
        track_name = track["track"]["name"]

        #Track id
        track_id = track["track"]["preview_url"]
        
        #Artist name
        artist_name = track["track"]["artists"][0]["name"]

        temp_dict = {"track_name": track_name, "track_url": track_id, "artist_name": artist_name}
        track_list["tracks"].append(temp_dict)


    track_list.update(serializer.data)
    return Response(track_list, status=status.HTTP_202_ACCEPTED)

