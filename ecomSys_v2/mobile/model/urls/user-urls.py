from django.urls import path
from model import views

urlpatterns = [
    path('mobiles', view = views.mobiles, name = 'mobile'),
]
