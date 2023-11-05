from rest_framework import serializers

from .models import ClientModel, EstablishmentModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientModel
        fields = ['id',
                  'username',
                  'email',
                  'password',
                  'first_name',
                  'last_name',
                  "birthday",
                  "sex",
                  ]


class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstablishmentModel
        fields = ['username',
                  'email',
                  'password',
                  "name",
                  "address",
                  "city",
                  "country",
                  "description",
                  "rut",
                  "verified"
                  ]


class EstablishmentQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = EstablishmentModel
        fields = ["name",
                  "address",
                  "city",
                  "country",
                  "description",
                  "rut",
                  "verified"
                  ]
