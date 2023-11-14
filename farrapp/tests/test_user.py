import pytest
from faker import Faker
from factories import ClientModelFactory, DemoClientFactory, EstablishmentModelFactory, RatingFactory
from django.test import TestCase, Client
from api.models import ClientModel, EstablishmentModel
from api.serializers import UserUpdateInfoSerializer
import json

fake = Faker()


@pytest.mark.django_db
def test_duplicated_username():
    DemoClientFactory.create()
    with pytest.raises(Exception):
        DemoClientFactory.create()
    
class ClientModelTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        data={
            "user_type":"client",
            "username":"scrumslave",
            "email": "example@as.com011",
            "password":"pass",
            "first_name": "Supu",
            "last_name":"Tamadre",
            "birthday":"2001-01-01",
            "sex":"f",
            "categories":[
                         {"name":"Reggue",
                            "type":"M"}
                        ]
            }
        response = self.client.post('http://127.0.0.1:8000/api/signup/client/', json.dumps(data), content_type='application/json')
        data = response.json()
        self.token = data.get('token')
        self.username = data.get('username')
        self.password = "pass"
        self.rs = response.status_code
    
    def test_signup_empty_user_type (self):
        data={
            "username":"scrumslavez",
            "email": "example@as.com0111",
            "password":"pass",
            "first_name": "Supu",
            "last_name":"Tamadre",
            "birthday":"2001-01-01",
            "sex":"f",
            "categories":[
                         {"name":"Reggue",
                            "type":"M"}
                        ]
            }
            
        response = self.client.post('http://127.0.0.1:8000/api/signup//', json.dumps(data), content_type='application/json')
        assert response.status_code==404

    def test_signup_wrong_user_type (self):
        data={
            "user_type":"pepapig",
            "username":"scrumslaves",
            "email": "example@as.com0121",
            "password":"pass",
            "first_name": "Supu",
            "last_name":"Tamadre",
            "birthday":"2001-01-01",
            "sex":"f",
            "categories":[
                         {"name":"Reggue",
                            "type":"M"}
                        ]
            }
        response = self.client.post('http://127.0.0.1:8000/api/signup/pepapig/', json.dumps(data), content_type='application/json')
        data = response.json()
        assert data.get('error') == 'User type not found'

    def test_signup_valid(self):
        assert self.rs == 201

    def test_login_incorrect_type_user (self):
        data = {
            "user_type":"establishment",
            "username":self.username,
            "password":self.password
        }
        response = self.client.post('http://127.0.0.1:8000/api/login/establishment/', json.dumps(data), content_type='application/json')
        assert response.status_code == 404

    def test_login_invalid (self):
        data = {
            "user_type":"client",
            "username":self.username,
            "password":"wrongpass"
        }
        response = self.client.post('http://127.0.0.1:8000/api/login/client/', json.dumps(data), content_type='application/json')
        data = response.json()
        assert data.get('error') == 'Wrong password'

    def test_login_valid (self):
        data = {
            "user_type":"client",
            "username":self.username,
            "password":self.password
        }
        response = self.client.post('http://127.0.0.1:8000/api/login/client/', json.dumps(data), content_type='application/json')
        data = response.json()

        assert response.status_code == 200

    def test_no_authentication (self):
        response=self.client.get('http://127.0.0.1:8000/api/establishments_list/')
        assert response.status_code == 401

    def test_establishment_list(self):
        headers = {'Authorization':f'Token {self.token}'}
        response=self.client.get('http://127.0.0.1:8000/api/establishments_list/', headers=headers)
        assert response.status_code == 200

    def test_update_preferences_valid (self):
        for i in range(20):
            rnd_client_data = ClientModelFactory.create()
            serializer_data = UserUpdateInfoSerializer(rnd_client_data).data
            json_data = json.dumps(serializer_data)
            headers = {'Authorization': f'Token {self.token}'}
            response = self.client.put('http://127.0.0.1:8000/api/update_pref/client/', data=json_data, content_type='application/json', headers=headers)
            cur_user = ClientModel.objects.get(username=self.username)

            assert response.status_code==202
            assert cur_user.first_name == rnd_client_data.first_name
            assert cur_user.last_name == rnd_client_data.last_name
            assert cur_user.sex == rnd_client_data.sex
            
            """
            for i in cur_user.categories.all():
                print (i.pk, i.name, i.type)
            for i in rnd_client_data.categories.all():
                print (i.pk, i.name, i.type)
            """
            assert list(cur_user.categories.all()) == list(rnd_client_data.categories.all())
            
    def test_search_establishment (self):
        for i in range(100):
            rnd_establishment = EstablishmentModelFactory.create()
            headers = {'Authorization': f'Token {self.token}'}
            path = f'http://127.0.0.1:8000/api/search_query/?name={rnd_establishment.name}'
            #print (path)
            response = self.client.get(path, headers=headers)
            data = response.json()
            assert data[0].get('name').startswith(rnd_establishment.name)

    def test_rating (self):
        for i in range (100):
            RatingFactory.create()

        cur_rate = EstablishmentModel.objects.get(pk = 3).overall_rating
        cur_reviews = EstablishmentModel.objects.get(pk = 3).number_of_reviews

        data = {
            "establishment_id":3,
            "rating":4
        }
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.put('http://127.0.0.1:8000/api/rate/', data=json.dumps(data), content_type='application/json',headers=headers)
        assert response.status_code == 202

        assert cur_rate + 4 == EstablishmentModel.objects.get(pk = 3).overall_rating
        assert cur_reviews + 1 == EstablishmentModel.objects.get(pk = 3).number_of_reviews

        data = {
            "establishment_id":3,
            "rating":1
        }
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.put('http://127.0.0.1:8000/api/rate/', data=json.dumps(data),content_type='application/json', headers=headers)
        assert response.status_code == 202

        assert cur_rate + 1 == EstablishmentModel.objects.get(pk = 3).overall_rating
        assert cur_reviews + 1 == EstablishmentModel.objects.get(pk = 3).number_of_reviews