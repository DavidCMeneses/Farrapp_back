from django.urls import path

from . import views

urlpatterns = [
    path('login/<str:user_type>/', views.login, name="api-login"),
    path('signup/<str:user_type>/', views.signup, name="api-signup"),
    path('search_query/', views.search_query, name = 'search_query'),
    path('establishments_list/', views.establishments_list, name="api-establishments-list"),
    path('check_auth/', views.check_auth, name="api-check-auth"),
    path('update_pref/<str:user_type>/', views.update_preferences, name="api-update-preferences"),
    path('delete_user/<str:user_type>/', views.delete_user, name="api-delete-user"),
    path('rating/', views.rate, name = "api-rate"),
    path('establishment_vis/<str:establishment_id>/', views.establishment_vis, name = "establishment_vis"),
]
