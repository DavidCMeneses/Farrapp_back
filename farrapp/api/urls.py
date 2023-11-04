from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="api-login"),
    path('signup/', views.signup_user, name="api-signup"),
    path('signup_est/', views.signup_Establishment, name="api-signup-est"),
    path('test/', views.test, name="api-test"),
]
