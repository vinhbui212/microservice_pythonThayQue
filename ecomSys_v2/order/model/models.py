from django.db import models

# Create your models here.

PAYMENT_STATUS = {
    'PENDING': 0,
    'DONE': 1
}

ORDER_STATUS = {
    'PENDING': 0,
    'PROCESSING': 1,
    'DELIVERING': 2,
    'DELIVERED': 3,
    'CANCELED': 4
}

PAYMENT_METHOD = {
    'CASH': 0,
    'CREDIT_CARD': 1
}


class Order(models.Model):
    user_id = models.PositiveBigIntegerField()
    total = models.PositiveBigIntegerField()
    status = models.PositiveIntegerField(default = ORDER_STATUS['PENDING'])
    payment_status = models.PositiveIntegerField(default = PAYMENT_STATUS['PENDING'])
    payment_method = models.PositiveIntegerField(default = PAYMENT_METHOD['CASH'])
    shipping_address = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    deleted = models.PositiveBigIntegerField(default = 0)

    class Meta:
        db_table = 'orders'
        verbose_name_plural = 'Orders'

    ordering = ['-created_at']

    def __str__(self):
        return str(self.pk)
