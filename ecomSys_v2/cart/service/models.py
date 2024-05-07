from django.db import models

# Create your models here.

PRODUCT_STATUS = {
    'PENDING': 0,
    'DONE': 1,
    'DELETED': 2,
    'EXPIRED': 3
}

PRODUCT_TYPE = {
    'BOOK': 0,
    'MOBILE': 1,
    'CLOTHES': 2
}


class Cart(models.Model):
    customer_id = models.CharField(max_length = 255)
    product_id = models.CharField(max_length = 255)
    quantity = models.PositiveBigIntegerField()
    product_status = models.PositiveIntegerField(help_text = 'Status of product in cart',
                                                 default = PRODUCT_STATUS['PENDING'])
    product_type = models.PositiveIntegerField()
    product_price = models.PositiveBigIntegerField(default = None, blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    deleted = models.PositiveBigIntegerField(default = 0)

    class Meta:
        db_table = 'carts'
        verbose_name_plural = 'Carts'

    ordering = ['-created_at']
