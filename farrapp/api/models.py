from django.db import models

# Create your models here.

class User_account (models.Model):
    username = models.CharField(max_length = 20, unique = True)
    email = models.EmailField(max_length = 50, unique = True)
    password = models.CharField(max_length = 20)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)

class Client (models.Model):
    birthday = models.DateField()
    sex = models.CharField(max_length = 1)
    user_id = models.OneToOneField(User_account, on_delete = models.CASCADE)

class Playlist (models.Model):
    link = models.URLField()


class Establishment (models.Model):
    name = models.CharField(max_length = 30)
    adress = models.CharField(max_length = 50)
    city = models.CharField(max_length = 20)
    country = models.CharField(max_length = 20)
    description = models.CharField(max_length = 2000)
    number_of_reviews = models.IntegerField()
    overall_rating = models.IntegerField()
    rut = models.BigIntegerField()
    verified = models.BooleanField()
    user_id = models.OneToOneField(User_account, on_delete = models.CASCADE)
    playlist_id = models.ForeignKey(Playlist, on_delete = models.PROTECT)
    
class Rating (models.Model):
    stars = models.SmallIntegerField()
    client_id = models.ForeignKey(Client, on_delete = models.CASCADE)
    establishment_id = models.ForeignKey(Establishment, on_delete=models.CASCADE)

class Category (models.Model):
    name = models.CharField(max_length = 50)
    type = models.CharField(max_length = 1)

class User_category (models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User_account, on_delete=models.CASCADE)

class Day_week (models.Model):
    name = models.CharField(max_length = 15)

class Image (models.Model):
    link = models.URLField()

class Establishment_img (models.Model):
    typ = models.CharField(max_length = 10)
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    establishment_id = models.ForeignKey(Establishment, on_delete=models.CASCADE)

class Establishment_schedule (models.Model):
    schedule_open = models.TimeField()
    schadule_close = models.TimeField()
    day_id = models.ForeignKey(Day_week, on_delete=models.CASCADE)
    establishment_id = models.ForeignKey(Establishment, on_delete=models.CASCADE)

class Ej_establishment (models.Model):
    name = models.CharField(max_length = 50)

class Trie (models.Model):
    node_from = models.IntegerField()
    let = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['node_from', 'let']),
        ]

class Node_establishment (models.Model):
    node = models.IntegerField()
    establishment_id = models.ForeignKey(Ej_establishment, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['node']),
        ]

