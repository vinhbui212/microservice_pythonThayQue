from django.utils import timezone
from djongo import models

from category.models import Category

# Create your models here.

MOBILE_STATUS = {
    'UNAVAILABLE': 0,
    'AVAILABLE': 1
}


class Mobile(models.Model):
    _id = models.ObjectIdField()
    code = models.CharField(max_length = 50)
    name = models.CharField(max_length = 255)
    description = models.TextField(null = True, blank = True)
    price = models.PositiveBigIntegerField()
    old_price = models.PositiveBigIntegerField(default = None, null = True, blank = True)
    image = models.ImageField(upload_to = 'images/')
    status = models.PositiveIntegerField(default = MOBILE_STATUS['AVAILABLE'])
    quantity = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    deleted = models.PositiveBigIntegerField(default = 0)
    categories = models.ManyToManyField(Category)

    class Meta:
        db_table = 'mobile'
        verbose_name_plural = 'Mobile'

    ordering = ['-created_at']

    def __str__(self):
        return self.code
