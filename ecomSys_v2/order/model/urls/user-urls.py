from django.urls import path
from model import views

urlpatterns = [
    path('orders', views.my_orders),
    path('orders/create', views.create_order),
]
