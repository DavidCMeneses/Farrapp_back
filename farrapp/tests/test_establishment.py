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
            "username":"Portal 8000",
            "email": "example@as.com011112",
            "password":"pass",
            "name": "farrapp",
            "address":"su ",
            "city": "bogota",
            "country": "China",
            "description": "Lugar donde puedes tomar ¿qué esperabas?",
            "rut": 11111,
            "verified": "false",
            "categories": [{"name":"rock",
                            "type":"M"}],
            "schedules": [{"open":"7:30:59",
                            "close":"21:30:20",
                            "day":"mon"
                            }]
        }
        response = self.client.post('http://127.0.0.1:8000/api/signup/', json.dumps(data), content_type='application/json')
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
        response = self.client.post('http://127.0.0.1:8000/api/login/', json.dumps(data), content_type='application/json')
        assert response.status_code == 404

    def test_login_invalid (self):
        data = {
            "user_type":"establishment",
            "username":self.username,
            "password":"wrongpass"
        }
        response = self.client.post('http://127.0.0.1:8000/api/login/', json.dumps(data), content_type='application/json')
        data = response.json()
        assert data.get('error') == 'Wrong password'

    def test_login_valid (self):
        data = {
            "user_type":"establishment",
            "username":self.username,
            "password":self.password
        }
        response = self.client.post('http://127.0.0.1:8000/api/login/', json.dumps(data), content_type='application/json')
        data = response.json()

        assert response.status_code == 200

    """"
    def test_update_preferences_valid (self):
        for i in range(20):
            rnd_establihsment_data = EstablishmentModelFactory.create()
            serializer_data = EstablishmentUpdateInfoSerializer(rnd_establihsment_data).data
            additional_data = {"user_type":"establishment"}
            serializer_data = {**additional_data, **serializer_data}
            json_data = json.dumps(serializer_data)
            headers = {'Authorization': f'Token {self.token}'}
            response = self.client.put('http://127.0.0.1:8000/api/update_pref/', data=json_data, content_type='application/json', headers=headers)
            cur_user = EstablishmentModel.objects.get(username=self.username)

            assert response.status_code==202
            assert cur_user.name == rnd_establihsment_data.name
            assert cur_user.address == rnd_establihsment_data.address
            assert cur_user.city == rnd_establihsment_data.city
            assert cur_user.country == rnd_establihsment_data.country
            assert cur_user.description == rnd_establihsment_data.description
            assert list(cur_user.categories.all()) == list(rnd_establihsment_data.categories.all())
            assert list(cur_user.schedules.all()) == list(rnd_establihsment_data.schedules.all())
    """