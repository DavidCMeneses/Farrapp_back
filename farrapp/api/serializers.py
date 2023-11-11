from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer 

from .models import ClientModel, EstablishmentModel, Category, Schedule

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name',
                  'type'
                  ]
        
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['open',
                  'close',
                  'day'
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
            category = Category.objects.get_or_create(**i)
            if category != None :
                instance.categories.add(category)
        return instance


class EstablishmentSerializer(WritableNestedModelSerializer, 
                              serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    schedules = ScheduleSerializer(many=True)
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
                  "categories",
                  "schedules"
                  ]


class EstablishmentQuerySerializer(WritableNestedModelSerializer, 
                                   serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    schedules = ScheduleSerializer(many=True)
    class Meta:
        model = EstablishmentModel
        fields = ["name",
                  "address",
                  "city",
                  "country",
                  "description",
                  "rut",
                  "verified",
                  "categories",
                  "schedules"
                  ]
        

class EstablishmentUpdateInfoSerializer(WritableNestedModelSerializer, 
                                        serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    schedules = ScheduleSerializer(many=True)
    class Meta:
        model = EstablishmentModel
        fields = ["name",
                  "address",
                  "city",
                  "country",
                  "description",
                  "categories",
                  "schedules"
                  ]
        
    def update(self, instance, validated_data):
        categories_list = validated_data.get('categories')
        schedules_list = validated_data.get('schedules')

        instance.categories.clear()
        instance.schedules.clear()

        for element in categories_list:
            category = Category.objects.get_or_create(**element)
            if category != None :
                instance.categories.add(category[0])
        for element in schedules_list:
            schedule = Schedule.objects.get_or_create(**element)
            if schedule != None :
                instance.schedules.add(schedule[0])
                
        return instance