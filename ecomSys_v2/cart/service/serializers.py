from rest_framework import serializers
from service.models import Cart


class CartSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'product_id', 'quantity', 'product_type', 'product_status', 'product_price', 'created_at',
                  'updated_at', 'total']

    def get_total(self, obj):
        return int(obj.quantity) * int(obj.product_price)
