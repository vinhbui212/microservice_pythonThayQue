from django.urls import path
from service import views

urlpatterns = [
    # Book
    path('book/key', views.admin_search_by_key),

    # Mobile
    path('mobile/key', views.admin_search_by_key),

    # Clothes
    path('clothes/key', views.admin_search_by_key),
]
