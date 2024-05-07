import json

from cerberus import Validator
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view

from constants import PER_PAGE
from helpers import response_success, response_error, call_api
from model.models import Order, ORDER_STATUS, PAYMENT_STATUS
from model.requests import create_and_update_schema
from model.serializers import OrderSerializer
from order.decorators import verify_token, check_permission
from order_item.models import OrderItem


# Create your views here.
@verify_token
@api_view(['GET'])
def my_orders(request):
    orders = Order.objects.filter(deleted = 0, user_id = request.user_id)
    return response_success('Success', OrderSerializer(orders, many = True).data)


@verify_token
@api_view(['POST'])
def create_order(request):
    req = json.loads(request.body)
    payment_method = req['payment_method']
    shipping_address = req['shipping_address']
    cart_item_ids = req['cart_item_ids']

    total = 0
    result = call_api(request, 'http://127.0.0.1:8001/api/cart/items')
    if result and result['data']:
        items = [item for item in result['data'] if item['id'] in cart_item_ids]
        for item in items:
            total += item['quantity'] * item['product_price']

        validator = Validator(create_and_update_schema)
        try:
            with transaction.atomic():
                order = {
                    'user_id': request.user_id,
                    'total': total,
                    'status': ORDER_STATUS['PENDING'],
                    'payment_status': PAYMENT_STATUS['PENDING'],
                    'payment_method': payment_method,
                    'shipping_address': shipping_address
                }

                new_order = None
                if validator.validate(order):
                    new_order = Order.objects.create(**order)
                else:
                    return response_error('Error', status.HTTP_400_BAD_REQUEST, validator.errors)

                for item in items:
                    new_item = {
                        'order': new_order,
                        'product_id': item['product_id'],
                        'product_type': item['product_type'],
                        'quantity': item['quantity'],
                        'product_price': item['product_price']
                    }
                    OrderItem.objects.create(**new_item)

                # update product status in cart when created order successfully
                is_updated_cart = call_api(
                    request,
                    'http://127.0.0.1:8001/api/cart/update-product-status',
                    'patch',
                    {'cart_item_ids': cart_item_ids}
                )

                # create shipment
                is_created_shipment = call_api(
                    request,
                    'http://127.0.0.1:8003/api/shipments/create',
                    'post',
                    {'order_id': new_order.id if order else None}
                )

                # create payment
                # check if customer paid or not
                is_order_paid = call_api(
                    request,
                    f'http://127.0.0.1:8004/api/payments/{new_order.id}',
                    'get'
                )
                if json.loads(is_order_paid.content.decode('utf-8'))['status'] == 'Failed':
                    is_created_payment = call_api(
                        request,
                        'http://127.0.0.1:8004/api/payments/create',
                        'post',
                        {
                            'order_id': new_order.id if order else None,
                            'total': new_order.total,
                            'method': new_order.payment_method
                        }
                    )

                if is_updated_cart['status'] == 'Failed':
                    return response_error(is_updated_cart['message'], is_updated_cart['status_code'])
                if is_created_shipment['status'] == 'Failed':
                    return response_error(is_created_shipment['message'], is_created_shipment['status_code'])
                if is_created_payment['status'] == 'Failed':
                    return response_error(is_created_payment['message'], is_created_payment['status_code'])

                return response_success()
        except:
            response_error('', status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response_error('', status.HTTP_500_INTERNAL_SERVER_ERROR)


@verify_token
@check_permission
@api_view(['GET'])
def get_all_orders(request):
    q = request.GET.get('q')
    page_query = request.GET.get('page')
    sort_order = request.GET.get('sort_order')
    field = request.GET.get('field')
    customer_id = request.GET.get('customer_id')

    if sort_order and field:
        field = '-' + field if sort_order == 'desc' else field
    else:
        field = '-created_at'

    page = int(page_query) if page_query is not None else 1
    from_page = PER_PAGE * (page - 1)
    to_page = PER_PAGE

    orders = Order.objects.filter(deleted = 0).order_by(field)

    if q is not None:
        orders = orders.filter(pk = q.strip())

    if customer_id is not None:
        orders = orders.filter(user_id = customer_id)

    orders = orders[from_page:to_page]

    response_data = {
        'page': page,
        'per_page': PER_PAGE,
        'total': len(orders),
        'orders': OrderSerializer(orders, many = True).data
    }

    return response_success('Success', response_data)


@verify_token
@check_permission
@api_view(['PATCH'])
def update_status(request, id):
    try:
        new_status = json.loads(request.body)['status']
        if new_status not in ORDER_STATUS.values():
            return response_error(f"Order status must be in {ORDER_STATUS.values()}")

        order = Order.objects.get(pk = id, deleted = 0)
        order.status = new_status
        order.save()

        return response_success('Updated Successfully')
    except ObjectDoesNotExist:
        return response_error('Order does not exist', status.HTTP_404_NOT_FOUND)
    except:
        return response_error('Bad Request', status.HTTP_400_BAD_REQUEST)


@verify_token
@check_permission
@api_view(['DELETE'])
def delete(request, id):
    try:
        order = Order.objects.get(pk = id, deleted = 0)
        order.deleted = 1
        order.save()

        return response_success('Deleted Successfully')
    except ObjectDoesNotExist:
        return response_error('Order does not exist', status.HTTP_404_NOT_FOUND)
    except:
        return response_error('Bad Request', status.HTTP_400_BAD_REQUEST)
