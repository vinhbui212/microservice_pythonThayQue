from django.db import models

from model.models import Order

# Create your models here.

PRODUCT_TYPE = {
    'BOOK': 0,
    'MOBILE': 1,
    'CLOTHES': 2
}


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = 'items')
    product_id = models.CharField(max_length = 255)
    product_type = models.PositiveIntegerField()
    quantity = models.PositiveBigIntegerField()
    product_price = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    deleted = models.PositiveBigIntegerField(default = 0)

    class Meta:
        db_table = 'order_items'
        verbose_name_plural = 'OrderItems'

    ordering = ['-created_at']

    def __str__(self):
        return self
