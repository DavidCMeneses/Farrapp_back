from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name="api-login"),
    path('signup/', views.signup, name="api-signup"),
    path('search_query/', views.search_query, name = 'search_query'),
    path('establishments_list/', views.establishments_list, name="api-establishments-list"),
    path('check_auth/', views.check_auth, name="api-check-auth"),
    path('update_pref/', views.update_preferences, name="api-update-preferences"),
    path('delete_user/', views.delete_user, name="api-delete-user"),
    path('rate/', views.rate, name = "api-rate"),
]
