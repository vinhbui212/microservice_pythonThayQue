from django.urls import path
from model import views

urlpatterns = [
    path('orders', views.get_all_orders),
    path('orders/<int:id>/update-status', views.update_status),
    path('orders/<int:id>/delete', views.delete),
]
