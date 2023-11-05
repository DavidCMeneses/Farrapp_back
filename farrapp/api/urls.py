from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name="api-login"),
    path('signup/', views.signup, name="api-signup"),
    path('establishments_list/', views.establishments_list, name="api-establishments-list"),
    path('check_auth/', views.check_auth, name="api-check-auth"),
]
