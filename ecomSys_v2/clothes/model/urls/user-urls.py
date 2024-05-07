from django.urls import path
from model import views

urlpatterns = [
    path('clothes', view = views.clothes, name = 'clothes'),
]
