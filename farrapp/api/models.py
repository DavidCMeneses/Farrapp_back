from django.db import models

from .Conejito_Auth import *


class ClientModel(AbstractCustomUser):
    birthday = models.DateField()
    sex = models.CharField(max_length=1)


class Establishment(AbstractCustomUser):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    description = models.CharField(max_length=2000)
    number_of_reviews = models.IntegerField(default=0)
    overall_rating = models.IntegerField(default=5)
    rut = models.BigIntegerField()
    verified = models.BooleanField()
    # playlist_id = models.ForeignKey(Playlist, on_delete=models.PROTECT)


"""
class Playlist(models.Model):
    link = models.URLField()


class Rating(models.Model):
    stars = models.SmallIntegerField()
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    establishment_id = models.ForeignKey(Establishment, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=1)


class User_category(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Client, on_delete=models.CASCADE)


class Day_week(models.Model):
    name = models.CharField(max_length=15)


class Image(models.Model):
    link = models.URLField()


class Establishment_img(models.Model):
    typ = models.CharField(max_length=10)
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    establishment_id = models.ForeignKey(Establishment, on_delete=models.CASCADE)


class Establishment_schedule(models.Model):
    schedule_open = models.TimeField()
    schadule_close = models.TimeField()
    day_id = models.ForeignKey(Day_week, on_delete=models.CASCADE)
    establishment_id = models.ForeignKey(Establishment, on_delete=models.CASCADE)


class Ej_establishment(models.Model):
    name = models.CharField(max_length=50)


class Trie(models.Model):
    node_from = models.IntegerField()
    let = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['node_from', 'let']),
        ]


class Node_establishment(models.Model):
    node = models.IntegerField()
    establishment_id = models.ForeignKey(Ej_establishment, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['node']),
        ]
"""
