from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="api-login"),
    path('signup/', views.signup, name="api-signup"),
    path('test/', views.test, name="api-test"),
]
