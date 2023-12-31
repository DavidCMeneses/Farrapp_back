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

from .stats import xlsx_maker, send_email_w_attachment

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

        if len(name) > 0:
            matched_list = search_est(name)
            matched_establishments = EstablishmentModel.objects.filter(pk__in=matched_list).prefetch_related("categories")
            position_map = {pk: pos for pos, pk in enumerate(matched_list)}

            matched_establishments = sorted(
                matched_establishments,
                key=lambda obj: position_map[obj.pk]  
            )
            
        else:
            mixx = music + type_est
            matched_establishments = EstablishmentModel.objects.filter(categories__name__in=mixx).prefetch_related("categories").distinct()

            #print (matched_establishments)
        
        music_set = set(music)
        type_est_set = set(type_est)

        #return Response({'al toque':'mi rey'}, status=status.HTTP_200_OK)

        pagin_results = []
        for cur_establishment in matched_establishments:
            string_preferences = ''
            
            
            for cat in cur_establishment.categories.all():
                if cat.name in music_set:
                    string_preferences = string_preferences + cat.name
                    break
            for cat in cur_establishment.categories.all():
                if cat.name in type_est_set:
                    if string_preferences != '':
                        string_preferences = string_preferences + ', '
                    string_preferences = string_preferences + cat.name
                    break
            
            
            rating = 5
            if cur_establishment.number_of_reviews > 0:
                rating = cur_establishment.overall_rating/cur_establishment.number_of_reviews
            
            '''
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
            song = {"track_name":track_name, "track_url":track_id, "artist_name":artist_name}
            '''

            pagin_results.append({"name":cur_establishment.name,
                                    "id":cur_establishment.pk,
                                    "address":cur_establishment.address,
                                    "city":cur_establishment.city,
                                    "preferences":string_preferences,
                                    "rating":rating, 
                                    "image_url":cur_establishment.image_url})



        if len(name) == 0:
            if sort_param == "rating":
                pagin_results = sorted(pagin_results, key=lambda x: x['rating'], reverse=True)
            elif sort_param == "asc" or sort_param == "desc":

                pagin_results = sorted(pagin_results, key = lambda x: x['name'], reverse = (sort_param == "desc"))
                
        
        request.session['pagin_results'] = pagin_results

    num_pa = 5
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
    user_rating = -1
    try:
        client_r = ClientModel.objects.get(username=request.user.username)
        Visualizations.objects.get_or_create(client=client_r, establishment=establishment)
        try:
            cur_rate = Rating.objects.get(client=client_r, establishment=establishment)
            user_rating = cur_rate.stars
        except ObjectDoesNotExist:
            user_rating = -1
    except ObjectDoesNotExist:
        user_rating = -1

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
        cid = os.getenv('CID_farrapp')
        secret = os.getenv('SECRET_farrapp')

        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        playlist_link = "https://open.spotify.com/playlist/37i9dQZF1DZ06evO0yp56w?si=ee44bc7d55d24e44"
        playlist_URI = playlist_link.split("/")[-1].split("?")[0]
        playlist_name = sp.playlist(playlist_id=playlist_URI, fields="name")["name"]

    # Json package
    serializer = EstablishmentInfoSerializer(establishment)

    # Rating
    if establishment.number_of_reviews != 0:
        rating = establishment.overall_rating / establishment.number_of_reviews
    else:
        rating = 5

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
def stats(request, establishment_id):

    filename = "data.xlsx"

    ans_list = []
    sex_list = []
    age_list = []
    music_list = []
    categ_list = []

    for i in Visualizations.objects.filter(establishment__pk = establishment_id):
        today = datetime.today()
        age = today.year - i.client.birthday.year - (
                (today.month, today.day) < (i.client.birthday.month, i.client.birthday.day))
        sex_list.append(i.client.sex)
        age_list.append(age)
        for j in i.client.categories.all():
            if j.type == 'M':
                music_list.append(j.name)
            else:
                categ_list.append(j.name)

    ans_list.append(sex_list)
    ans_list.append(age_list)
    ans_list.append(music_list)
    ans_list.append(categ_list)

    xlsx_maker(filename, ans_list, ["Sexes", "#", "Ages", "#", "Music", "#", "Categories", "#"])

    # who are we sending this email to?
    to = "drogindito@gmail.com"

    # what is our subject line?
    subject = "FARRAPP User-Data"

    # what is the body of the email?
    body = "Hola, ¡Te escribimos de Farrapp! \nTe envíamos un correo con tus datos de este mes, esperamos que te sea útil, \nRecuerda que puedes contactarnos por este correo, \n¡y que la farra nunca pare!"
    
    send_email_w_attachment(to, subject, body, filename)

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
