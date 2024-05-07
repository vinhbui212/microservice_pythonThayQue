from django.urls import path, include
from service import views

urlpatterns = [
    # Book
    path('book/key', views.search_by_key),
    path('book/voice', views.search_by_voice),

    # Mobile
    path('mobile/key', views.search_by_key),
    path('mobile/voice', views.search_by_voice),

    # Clothes
    path('clothes/key', views.search_by_key),
    path('clothes/voice', views.search_by_voice),
]
