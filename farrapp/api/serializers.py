from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import ClientModel, EstablishmentModel, Category, Schedule, Rating


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
        fields = ['username',
                  'email',
                  'password',
                  'first_name',
                  'last_name',
                  "birthday",
                  "sex",
                  "categories"
                  ]

    def create (self, validated_data):
        categories = validated_data.pop('categories', None)
        instance = super(UserSerializer, self).create(validated_data)

        if categories is not None:
            for element in categories:
                category = Category.objects.get_or_create(**element)
                instance.categories.add(category[0])
        
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
                  "schedules",
                  "playlist_id",
                  "image_url"
                  ]
        
    def create (self, validated_data):
        categories = validated_data.pop('categories', None)
        schedules = validated_data.pop('schedules', None)
        instance = super(EstablishmentSerializer, self).create(validated_data)

        if categories is not None:
            for element in categories:
                category = Category.objects.get_or_create(**element)
                instance.categories.add(category[0])
        
        if schedules is not None:
            for element in schedules:
                schedule = Schedule.objects.get_or_create(**element)
                instance.schedules.add(schedule[0])

        return instance


class EstablishmentQuerySerializer(WritableNestedModelSerializer,
                                   serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    schedules = ScheduleSerializer(many=True)

    class Meta:
        model = EstablishmentModel
        fields = ["pk",
                  "name",
                  "address",
                  "city",
                  "country",
                  "description",
                  "rut",
                  "verified",
                  "overall_rating",
                  "number_of_reviews",
                  "categories",
                  "schedules",
                  "playlist_id",
                  "image_url"
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

        # print(validated_data)

        categories_list = validated_data.get('categories')
        instance.categories.clear()

        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.sex = validated_data.get('sex')

        for i in categories_list:
            category = Category.objects.get_or_create(**i)
            if category is not None:
                instance.categories.add(category[0])
        return instance


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
                  "schedules",
                  "playlist_id",
                  "image_url"
                  ]

    def update(self, instance, validated_data):
        categories_list = validated_data.get('categories')
        schedules_list = validated_data.get('schedules')

        instance.categories.clear()
        instance.schedules.clear()

        instance.name = validated_data.get('name')
        instance.address = validated_data.get('address')
        instance.city = validated_data.get('city')
        instance.country = validated_data.get('country')
        instance.description = validated_data.get('description')
        instance.playlist_id = validated_data.get('playlist_id')
        instance.image_url = validated_data.get('image_url')

        for element in categories_list:
            category = Category.objects.get_or_create(**element)
            instance.categories.add(category[0])
        for element in schedules_list:
            schedule = Schedule.objects.get_or_create(**element)
            instance.schedules.add(schedule[0])

        return instance
