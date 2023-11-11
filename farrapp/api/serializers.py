from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer 

from .models import ClientModel, EstablishmentModel, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name',
                  'type'
                  ]

class UserSerializer(WritableNestedModelSerializer, 
                     serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
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
                  "categories"
                  ]
        

class UserUpdateInfoSerializer(WritableNestedModelSerializer, 
                                serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    class Meta:
        model = ClientModel
        fields = ['first_name',
                  'last_name',
                  "sex",
                  "categories"
                  ]
        
    def update(self, instance, validated_data):
        categories_list = validated_data.get('categories')
        instance.categories.clear()
        for i in categories_list:
            c_name = i.get('name')
            category = Category.objects.get(name=c_name)
            if category != None :
                instance.categories.add(category)
        return instance


class EstablishmentSerializer(WritableNestedModelSerializer, 
                              serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
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
                  "verified",
                  "categories"
                  ]


class EstablishmentQuerySerializer(WritableNestedModelSerializer, 
                                   serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    class Meta:
        model = EstablishmentModel
        fields = ["name",
                  "address",
                  "city",
                  "country",
                  "description",
                  "rut",
                  "verified",
                  "categories"
                  ]
        

class EstablishmentUpdateInfoSerializer(WritableNestedModelSerializer, 
                                        serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    class Meta:
        model = EstablishmentModel
        fields = ["name",
                  "address",
                  "city",
                  "country",
                  "description",
                  "categories"
                  ]
        
    def update(self, instance, validated_data):
        categories_list = validated_data.get('categories')
        instance.categories.clear()
        for i in categories_list:
            c_name = i.get('name')
            category = Category.objects.get(name=c_name)
            if category != None :
                instance.categories.add(category)
        return instance