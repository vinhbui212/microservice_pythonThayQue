from rest_framework import serializers
from helpers import call_api, response_error
from model.models import Payment
from rest_framework import status


class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        exclude = ['deleted']

    def __init__(self, *args, **kwargs):
        super(PaymentSerializer, self).__init__(*args, **kwargs)
        if not self.context.get('include_order', False):
            self.fields.pop('order', None)
        else:
            self.fields.pop('order_id', None)

    def get_order(self, obj):
        request = self.context.get('request')
        result = call_api(
            request,
            'http://127.0.0.1:8001/api/orders',
            'get',
            None,
            {
                'q': obj.order_id
            }
        )

        belong_order = result['data'][0] if result['data'] else None
        if not belong_order:
            return response_error('Bad Request', status.HTTP_400_BAD_REQUEST)

        return belong_order
