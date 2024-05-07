from rest_framework import serializers

from order_item.models import OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ['deleted', 'order']
