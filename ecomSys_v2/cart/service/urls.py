from django.urls import path
from service import views

urlpatterns = [
    path('items', views.get_all_products_in_cart),
    path('add-item', views.add_to_cart),
    path('delete-item/<int:id>', views.delete_item),
    path('update-product-status', views.update_product_status)
]
