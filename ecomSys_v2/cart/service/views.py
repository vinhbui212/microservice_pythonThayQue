import json

from cerberus import Validator
from django.db.models import Q
from rest_framework.decorators import api_view
from helpers import call_api, response_error, response_success
from cart.decorators import verify_token
from service.models import Cart, PRODUCT_STATUS, PRODUCT_TYPE
from service.requests import create_and_update_schema
from service.serializers import CartSerializer
from rest_framework import status


# Create your views here.


@verify_token
@api_view(['GET'])
def get_all_products_in_cart(request):
    user_id = request.current_user['id']

    items = (
        Cart.objects
        .filter(Q(product_status = PRODUCT_STATUS['PENDING']) | Q(product_status = PRODUCT_STATUS['EXPIRED']),
                deleted = 0, customer_id = user_id)
        .order_by('-created_at')
    )

    return response_success(
        '',
        CartSerializer(items, many = True).data
    )


@verify_token
@api_view(['POST'])
def add_to_cart(request):
    user_id = request.current_user['id']
    quantity = int(request.POST.get('quantity'))
    product_type = int(request.POST.get('product_type'))
    product_id = request.POST.get('product_id')

    products = {}
    key = ''
    if product_type == PRODUCT_TYPE['BOOK']:
        products = call_api(request, 'http://127.0.0.1:8001/books')
        key = 'books'
    elif product_type == PRODUCT_TYPE['CLOTHES']:
        products = call_api(request, 'http://127.0.0.1:8000/clothes')
        key = 'clothes'
    elif product_type == PRODUCT_TYPE['MOBILE']:
        products = call_api(request, 'http://127.0.0.1:8000/mobiles')
        key = 'mobiles'

    product = next((item for item in products['data'][key] if item.get('_id') == product_id), None)

    item = {
        'product_id': product_id,
        'customer_id': user_id,
        'product_type': product_type,
        'product_price': product['price'],
        'quantity': quantity,
        'product_status': PRODUCT_STATUS['PENDING']
    }

    validator = Validator(create_and_update_schema)
    if validator.validate(item):
        try:
            item = Cart.objects.filter(
                product_id = product_id, deleted = 0,
                product_status = PRODUCT_STATUS['PENDING'],
                customer_id = user_id
            )

            exist_item = item.filter(product_price = product['price'])[0]
            exist_item_with_old_price = item.exclude(product_price = product['price'])[0]

            if exist_item_with_old_price is not None:
                exist_item_with_old_price.product_status = PRODUCT_STATUS['EXPIRED']
                exist_item_with_old_price.save()

            if exist_item is not None:
                exist_item.quantity += quantity
                exist_item.save()
            else:
                Cart.objects.create(**item)

            return response_success('Added successfully')
        except Exception as e:
            return response_error('Error', status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response_error('Error', status.HTTP_400_BAD_REQUEST, validator.errors)


@verify_token
@api_view(['DELETE'])
def delete_item(request, id):
    item = Cart.objects.get(pk = id, deleted = 0)
    if not item:
        return response_error('Item does not exist.', status.HTTP_400_BAD_REQUEST)

    if item.product_status == PRODUCT_STATUS['DELETED'] or item.product_status == PRODUCT_STATUS['DONE']:
        return response_error('Item has been deleted or bought')

    item.product_status = PRODUCT_STATUS['DELETED']
    item.save()

    return response_success('Deleted Successfully')


@verify_token
@api_view(['PATCH'])
def update_product_status(request):
    try:
        cart_item_ids = json.loads(request.body)['cart_item_ids']
        for item_id in cart_item_ids:
            item = Cart.objects.get(pk = item_id, deleted = 0, product_status = PRODUCT_STATUS['PENDING'])
            item.product_status = PRODUCT_STATUS['DONE']
            item.save()

        return response_success('Updated Successfully')
    except Exception as e:
        return response_error('One of items does not exist.', status.HTTP_400_BAD_REQUEST)
