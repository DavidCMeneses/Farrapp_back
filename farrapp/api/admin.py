from django.contrib import admin

from .models import ClientModel, EstablishmentModel


@admin.register(ClientModel)
class ClientModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'birthday', 'sex')


@admin.register(EstablishmentModel)
class ClientModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', )

