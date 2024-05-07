from rest_framework import serializers

from model.models import Order
from order_item.serializers import OrderItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        exclude = ['deleted']

    def get_items(self, obj):
        items = obj.items.all()
        return OrderItemSerializer(items, many = True).data
