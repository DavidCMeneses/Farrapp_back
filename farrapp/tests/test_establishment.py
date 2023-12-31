import pytest
from faker import Faker
from factories import ClientModelFactory, DemoClientFactory, EstablishmentModelFactory, RatingFactory
from django.test import TestCase, Client
from api.models import ClientModel, EstablishmentModel
from api.serializers import EstablishmentUpdateInfoSerializer
import json

fake = Faker()

class EstablishmentModelTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        data={
            "user_type":"establishment",
            "username":"user001",
            "email": "email001@gmail.com",
            "password":"pass",
            "name": "theatron",
            "address":"la esquina de las divinas",
            "city": "bogota",
            "country": "China",
            "description": "Lugar donde puedes tomar ¿qué esperabas?",
            "rut": 11111,
            "verified": "false",
            "image_url": "jijijaja.com",
            "playlist_id": "https://open.spotify.com/playlist/37i9dQZF1DWSpF87bP6JSF",
            "categories": [{"name":"reggaeton",
                            "type":"M"},
			   {"name":"bachata",
                            "type":"M"},
			   {"name":"denbow",
                            "type":"M"}, 
			   {"name":"bar gay",
                            "type":"E"}, 
			   {"name":"club de baile",
                            "type":"E"},
			   {"name":"bar",
                            "type":"E"}],
            "schedules": [{"open":"20:30:00",
                            "close":"03:00:00",
                            "day":"friday"
                            },
			  {"open":"21:00:00",
			   "close":"04:30:00",
		  	   "day":"saturday"}]
            }
        response = self.client.post('http://127.0.0.1:8000/api/signup/establishment/', json.dumps(data), content_type='application/json')
        data = response.json()
        self.token = data.get('token')
        self.username = data.get('username')
        self.password = "pass"
        self.rs = response.status_code
    
    def test_signup_valid(self):
        assert self.rs == 201

    def test_login_incorrect_type_user (self):
        data = {
            "user_type":"client",
            "username":self.username,
            "password":self.password
        }
        response = self.client.post('http://127.0.0.1:8000/api/login/client/', json.dumps(data), content_type='application/json')
        assert response.status_code == 404

    def test_login_invalid (self):
        data = {
            "user_type":"establishment",
            "username":self.username,
            "password":"wrongpass"
        }
        response = self.client.post('http://127.0.0.1:8000/api/login/establishment/', json.dumps(data), content_type='application/json')
        data = response.json()
        assert data.get('error') == 'Wrong password'

    def test_login_valid (self):
        data = {
            "user_type":"establishment",
            "username":self.username,
            "password":self.password
        }
        response = self.client.post('http://127.0.0.1:8000/api/login/establishment/', json.dumps(data), content_type='application/json')
        data = response.json()

        assert response.status_code == 200

    
    def test_update_preferences_valid (self):
        for i in range(1):
            rnd_establihsment_data = EstablishmentModelFactory.create()
            serializer_data = EstablishmentUpdateInfoSerializer(rnd_establihsment_data).data
            json_data = json.dumps(serializer_data)
            headers = {'Authorization': f'Token {self.token}'}
            #print (json_data)
            response = self.client.put('http://127.0.0.1:8000/api/update_pref/establishment/', data=json_data, content_type='application/json', headers=headers)
            cur_user = EstablishmentModel.objects.get(username=self.username)

            assert response.status_code==202
            assert cur_user.name == rnd_establihsment_data.name
            assert cur_user.address == rnd_establihsment_data.address
            assert cur_user.city == rnd_establihsment_data.city
            assert cur_user.country == rnd_establihsment_data.country
            assert cur_user.description == rnd_establihsment_data.description
            assert list(cur_user.categories.all()) == list(rnd_establihsment_data.categories.all())
            assert list(cur_user.schedules.all()) == list(rnd_establihsment_data.schedules.all())
    