from django.db import models

# Create your models here.

PAYMENT_STATUS = {
    'PENDING': 0,
    'DONE': 1
}

PAYMENT_METHOD = {
    'CASH': 0,
    'CREDIT_CARD': 1
}


class Payment(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    mobile = models.CharField(max_length = 10)
    order_id = models.PositiveBigIntegerField()
    total = models.PositiveBigIntegerField()
    status = models.PositiveIntegerField(default = PAYMENT_STATUS['PENDING'])
    method = models.PositiveIntegerField(default = PAYMENT_METHOD['CASH'])
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    deleted = models.PositiveBigIntegerField(default = 0)

    class Meta:
        db_table = 'payments'
        verbose_name_plural = 'Payments'

    ordering = ['-created_at']

    def __str__(self):
        return str(self.pk)
