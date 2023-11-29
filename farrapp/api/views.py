from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime
from .Conejito_Auth import CustomToken, TokenAuthentication
from .models import ClientModel, EstablishmentModel, Rating, Category, Visualizations
from .serializers import UserSerializer, EstablishmentSerializer, EstablishmentQuerySerializer, \
    UserUpdateInfoSerializer, EstablishmentUpdateInfoSerializer, EstablishmentInfoSerializer

from .search import search_est

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import os
from dotenv import dotenv_values, load_dotenv


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
    return Response({'token': token.key, "username": serializer.data["username"], "id": serializer.data["pk"]},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def signup(request, user_type):
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
        return Response({'token': token.key, "username": serializer.data["username"], "id": serializer.data["pk"]},
                        status=status.HTTP_201_CREATED)
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
def search(request, page):
    if page == 1:
        name = request.GET['query']
        music = list(request.GET['filter_music'].split('|'))
        if request.GET['filter_music'] == '':
            music = []
        type_est = list(request.GET['establishment_filter'].split('|'))
        if request.GET['establishment_filter'] == '':
            type_est = []
        flag = request.GET['flag']
        sort_param = request.GET['sorted_by']

        if flag == "True":
            music = []
            type_est = []
            client_r = ClientModel.objects.get(username=request.user.username)
            print(client_r.username)
            for category in client_r.categories.all():
                if category.type == 'M':
                    music.append(category.name)
                if category.type == 'E':
                    type_est.append(category.name)

        # if music or type_est is not especified take all objects
        if len(music) == 0:
            music = []
            for i in Category.objects.all():
                if i.type == 'M':
                    music.append(i.name)
        if len(type_est) == 0:
            type_est = []
            for i in Category.objects.all():
                if i.type == 'E':
                    type_est.append(i.name)

        matched_establishments = []
        if len(name) > 0:
            matched_establishments = search_est(name)
        else:
            for i in EstablishmentModel.objects.all():
                matched_establishments.append(i.pk)

        match_establishment_category = [dict(), dict()]

        for i in music:
            establishment_music_i = EstablishmentModel.objects.filter(categories__name=i)
            for establishment in establishment_music_i:
                match_establishment_category[0].setdefault(establishment.pk, i)

        for i in type_est:
            establishment_type_est_i = EstablishmentModel.objects.filter(categories__name=i)
            for establishment in establishment_type_est_i:
                match_establishment_category[1].setdefault(establishment.pk, i)

        pagin_results = []
        for est in matched_establishments:
            cur_establishment = EstablishmentModel.objects.get(pk=est)
            if cur_establishment.pk in match_establishment_category[0] or cur_establishment.pk in \
                    match_establishment_category[1]:
                string_preferences = ''
                if cur_establishment.pk in match_establishment_category[0]:
                    string_preferences = string_preferences + match_establishment_category[0][cur_establishment.pk]
                if cur_establishment.pk in match_establishment_category[1]:
                    if string_preferences != '':
                        string_preferences = string_preferences + ', '
                    string_preferences = string_preferences + match_establishment_category[1][cur_establishment.pk]

                rating = 5
                if cur_establishment.number_of_reviews > 0:
                    rating = cur_establishment.overall_rating / cur_establishment.number_of_reviews

                try:
                    # Authentication - without user
                    cid = os.getenv('CID_farrapp')
                    secret = os.getenv('SECRET_farrapp')

                    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
                    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

                    playlist_link = cur_establishment.playlist_id
                    playlist_URI = playlist_link.split("/")[-1].split("?")[0]

                except:
                    return Response({'error': 'Invalid playlist'}, status=status.HTTP_404_NOT_FOUND)

                tracks = sp.playlist_tracks(playlist_URI)["items"]
                track_name = tracks[0]["track"]["name"]
                track_id = tracks[0]["track"]["preview_url"]
                artist_name = tracks[0]["track"]["artists"][0]["name"]
                song = {"track_name": track_name, "track_url": track_id, "artist_name": artist_name}

                pagin_results.append({"name": cur_establishment.name,
                                      "id": cur_establishment.pk,
                                      "address": cur_establishment.address,
                                      "city": cur_establishment.city,
                                      "preferences": string_preferences,
                                      "rating": rating,
                                      "image_url": cur_establishment.image_url,
                                      "song": song})

        if len(name) == 0:
            if sort_param == "rating":
                pagin_results = sorted(pagin_results, key=lambda x: x['rating'], reverse=True)
            elif sort_param == "asc" or sort_param == "desc":
                pagin_results = sorted(pagin_results, key=lambda x: x['name'], reverse=(sort_param == "desc"))

        request.session['pagin_results'] = pagin_results

    num_pa = 1
    tot_results = len(request.session['pagin_results'])
    npages = (tot_results + num_pa - 1) // num_pa
    results = []
    try:
        results = request.session['pagin_results'][(page - 1) * num_pa: min(tot_results, page * num_pa)]
    except PageNotAnInteger:
        return Response({'error': 'page requested is not integer'}, status=status.HTTP_400_BAD_REQUEST)
    except EmptyPage:
        return Response({'error': 'page requested is out of range'}, status=status.HTTP_400_BAD_REQUEST)

    data_to_return = {'pages': npages, 'results': results}

    return Response(data_to_return, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def rate(request):
    client_r = ClientModel.objects.get(username=request.user.username)
    establishment_r = EstablishmentModel.objects.get(pk=request.data.get('establishment_id'))
    stars = request.data.get('rating')
    try:
        cur_rate = Rating.objects.get(client=client_r, establishment=establishment_r)
        establishment_r.overall_rating += stars - cur_rate.stars
        cur_rate.stars = stars
        establishment_r.save()
        cur_rate.save()
    except ObjectDoesNotExist:
        Rating.objects.create(stars=stars, client=client_r, establishment=establishment_r)
        establishment_r.overall_rating += stars
        establishment_r.number_of_reviews += 1
        establishment_r.save()
    return Response({'user': request.user.username, 'establishment': establishment_r.name},
                    status=status.HTTP_202_ACCEPTED)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_preferences(request, user_type):
    # user_type = request.data.get('user_type', None)

    if user_type is None:
        return Response({'error': 'You must provide a user type'}, status=status.HTTP_404_NOT_FOUND)
    if user_type == 'client':
        obj = get_object_or_404(ClientModel, username=request.user.username)
        # print (obj)
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
def delete_user(request, user_type):
    # user_type = request.data.get('user_type', None)

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
    try:
        establishment = EstablishmentModel.objects.get(pk=establishment_id)
    except ObjectDoesNotExist:
        return Response({'error': 'invalid id'}, status=status.HTTP_404_NOT_FOUND)

    client_r = ClientModel.objects.get(username=request.user.username)

    Visualizations.objects.get_or_create(client=client_r, establishment=establishment)

    try:
        # Authentication - without user
        cid = os.getenv('CID_farrapp')
        secret = os.getenv('SECRET_farrapp')

        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        playlist_link = establishment.playlist_id
        playlist_URI = playlist_link.split("/")[-1].split("?")[0]
        playlist_name = sp.playlist(playlist_id=playlist_URI, fields="name")["name"]

    except:
        return Response({'error': 'Invalid playlist'}, status=status.HTTP_404_NOT_FOUND)

    # Json package
    serializer = EstablishmentInfoSerializer(establishment)

    # Rating
    if establishment.number_of_reviews != 0:
        rating = establishment.overall_rating / establishment.number_of_reviews
    else:
        rating = 5

    user_rating = -1
    try:
        cur_rate = Rating.objects.get(client=client_r, establishment=establishment)
        user_rating = cur_rate.stars
    except ObjectDoesNotExist:
        user_rating = -1

    track_list = {"user_rating": user_rating, "playlist_name": playlist_name, "tracks": [], "rating": rating}
    tracks = sp.playlist_tracks(playlist_URI)["items"]

    for i in range(0, min(5, len(tracks))):
        track = tracks[i]

        # Track name
        track_name = track["track"]["name"]

        # Track id
        track_id = track["track"]["preview_url"]

        # Artist name
        artist_name = track["track"]["artists"][0]["name"]

        temp_dict = {"track_name": track_name, "track_url": track_id, "artist_name": artist_name}
        track_list["tracks"].append(temp_dict)

    track_list.update(serializer.data)
    return Response(track_list, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def stats(request):
    ans_list = []
    for i in Visualizations.objects.all():
        today = datetime.today()
        age = today.year - i.client.birthday.year - (
                    (today.month, today.day) < (i.client.birthday.month, i.client.birthday.day))
        list_temp = [i.establishment.pk, i.client.sex, age]
        category_list = []
        for j in i.client.categories.all():
            category_list.append(j.name)
            category_list.append(j.type)
        list_temp.append(category_list)
        ans_list.append(list_temp)
    print(ans_list)
    return Response({"ok": "ok"}, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def fetch_self_data(request, user_type):
    if user_type is None:
        return Response({'error': 'You must provide a user type'}, status=status.HTTP_404_NOT_FOUND)
    if user_type == 'client':
        user = get_object_or_404(ClientModel, username=request.user.username)
        serializer = UserSerializer(instance=user)
    elif user_type == 'establishment':
        user = get_object_or_404(EstablishmentModel, username=request.user.username)
        serializer = EstablishmentSerializer(instance=user)
    else:
        return Response({'error': 'User type not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data, status=status.HTTP_200_OK)
