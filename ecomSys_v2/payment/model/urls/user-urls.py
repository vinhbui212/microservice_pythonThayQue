from django.urls import path
from model import views

urlpatterns = [
    path('<int:order_id>', views.get_my_order_payment),
    path('confirm', views.confirm_payment),
    path('create', views.create),
]
