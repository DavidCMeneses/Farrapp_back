# Generated by Django 4.2.6 on 2023-11-25 21:21

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
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.SmallIntegerField()),
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
            name='Visualizations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ClientModel',
            fields=[
                ('abstractcustomuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.abstractcustomuser')),
                ('birthday', models.DateField()),
                ('sex', models.CharField(max_length=1)),
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
                ('image_url', models.CharField(max_length=255)),
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
            name='UserCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.category')),
            ],
        ),
        migrations.CreateModel(
            name='EstablishmentImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ', models.CharField(max_length=10)),
                ('image_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.image')),
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
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['name'], name='api_categor_name_53a3ad_idx'),
        ),
        migrations.AddField(
            model_name='visualizations',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.clientmodel'),
        ),
        migrations.AddField(
            model_name='visualizations',
            name='establishment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.establishmentmodel'),
        ),
        migrations.AddField(
            model_name='usercategory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.clientmodel'),
        ),
        migrations.AddField(
            model_name='rating',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.clientmodel'),
        ),
        migrations.AddField(
            model_name='rating',
            name='establishment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.establishmentmodel'),
        ),
        migrations.AddField(
            model_name='establishmentmodel',
            name='categories',
            field=models.ManyToManyField(to='api.category'),
        ),
        migrations.AddField(
            model_name='establishmentmodel',
            name='schedules',
            field=models.ManyToManyField(to='api.schedule'),
        ),
        migrations.AddField(
            model_name='establishmentimg',
            name='establishment_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.establishmentmodel'),
        ),
        migrations.AddField(
            model_name='clientmodel',
            name='categories',
            field=models.ManyToManyField(to='api.category'),
        ),
        migrations.AddIndex(
            model_name='visualizations',
            index=models.Index(fields=['client', 'establishment'], name='api_visuali_client__d81719_idx'),
        ),
        migrations.AddIndex(
            model_name='rating',
            index=models.Index(fields=['client', 'establishment'], name='api_rating_client__ab5fc6_idx'),
        ),
    ]
