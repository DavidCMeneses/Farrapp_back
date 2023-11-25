<<<<<<< HEAD
# Generated by Django 4.2.6 on 2023-11-15 16:44
=======
# Generated by Django 4.2.6 on 2023-11-24 00:46
>>>>>>> 6569b45d6fd5efa83be0a7b03e178d818a6e76a7

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractCustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open', models.TimeField()),
                ('close', models.TimeField()),
                ('day', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ClientModel',
            fields=[
                ('abstractcustomuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.abstractcustomuser')),
                ('birthday', models.DateField()),
                ('sex', models.CharField(max_length=1)),
                ('categories', models.ManyToManyField(to='api.category')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
            },
            bases=('api.abstractcustomuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='EstablishmentModel',
            fields=[
                ('abstractcustomuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.abstractcustomuser')),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=2000)),
                ('number_of_reviews', models.IntegerField(default=0)),
                ('overall_rating', models.IntegerField(default=0)),
                ('rut', models.BigIntegerField()),
                ('verified', models.BooleanField(default=False)),
                ('playlist_id', models.CharField(max_length=255)),
                ('categories', models.ManyToManyField(to='api.category')),
                ('schedules', models.ManyToManyField(to='api.schedule')),
            ],
            options={
                'verbose_name': 'Establishment',
                'verbose_name_plural': 'Establishments',
            },
            bases=('api.abstractcustomuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CustomToken',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to='api.abstractcustomuser', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Token',
                'verbose_name_plural': 'Tokens',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.clientmodel')),
            ],
        ),
        migrations.CreateModel(
            name='EstablishmentImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ', models.CharField(max_length=10)),
                ('image_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.image')),
                ('establishment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.establishmentmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.SmallIntegerField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.clientmodel')),
                ('establishment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.establishmentmodel')),
            ],
            options={
                'indexes': [models.Index(fields=['client', 'establishment'], name='api_rating_client__ab5fc6_idx')],
            },
        ),
    ]
