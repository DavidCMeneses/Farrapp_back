from django.db import models

from .Conejito_Auth import *


class Category(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=1)


class Schedule(models.Model):
    schedule_open = models.TimeField()
    schedule_close = models.TimeField()
    day = models.CharField(max_length=3)


class ClientModel(AbstractCustomUser):
    birthday = models.DateField()
    sex = models.CharField(max_length=1)
    categories = models.ManyToManyField(Category)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class EstablishmentModel(AbstractCustomUser):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    description = models.CharField(max_length=2000)
    number_of_reviews = models.IntegerField(default=0)
    overall_rating = models.IntegerField(default=5)
    rut = models.BigIntegerField()
    verified = models.BooleanField()
    playlist_id = models.URLField()
    categories = models.ManyToManyField(Category)
    schedule = models.ManyToManyField(Schedule)

    class Meta:
        verbose_name = 'Establishment'
        verbose_name_plural = 'Establishments'


class Rating(models.Model):
    stars = models.SmallIntegerField()
    client_id = models.ForeignKey(ClientModel, on_delete=models.CASCADE)
    establishment_id = models.ForeignKey(EstablishmentModel, on_delete=models.CASCADE)


class UserCategory(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    user_id = models.ForeignKey(ClientModel, on_delete=models.CASCADE)


class Image(models.Model):
    link = models.URLField()


class EstablishmentImg(models.Model):
    typ = models.CharField(max_length=10)
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    establishment_id = models.ForeignKey(EstablishmentModel, on_delete=models.CASCADE)



