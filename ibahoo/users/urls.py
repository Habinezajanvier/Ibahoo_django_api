
from django.urls import path
from .views import AthenticatedUser, login, register

urlpatterns = [
    path('register', register),
    path('login', login),
    path('user', AthenticatedUser.as_view())
]