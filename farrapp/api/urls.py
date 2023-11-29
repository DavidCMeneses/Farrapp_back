from django.urls import path

from . import views

urlpatterns = [
    path('login/<str:user_type>/', views.login, name="api-login"),
    path('signup/<str:user_type>/', views.signup, name="api-signup"),
    path('search/<int:page>/', views.search, name='api-search'),
    path('establishments_list/', views.establishments_list, name="api-establishments-list"),
    path('check_auth/', views.check_auth, name="api-check-auth"),
    path('update_pref/<str:user_type>/', views.update_preferences, name="api-update-preferences"),
    path('delete_user/<str:user_type>/', views.delete_user, name="api-delete-user"),
    path('rate/', views.rate, name="api-rate"),
    path('fetch_info/<str:establishment_id>', views.fetch_establishment_info, name="api-fetch-info"),
    path('stats/', views.stats, name='api-stats'),
    path('user_info/<str:user_type>/', views.fetch_self_data, name='api-stats')
]
