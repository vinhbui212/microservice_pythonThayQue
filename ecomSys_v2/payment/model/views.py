import json
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework.decorators import api_view
from constants import PER_PAGE
from helpers import response_success, response_error
from model.models import Payment, PAYMENT_STATUS
from model.serializers import PaymentSerializer
from payment.decorators import verify_token, check_permission
from rest_framework import status as http_status


# Create your views here.
def create_payment(request, status):
    try:
        req = json.loads(request.body)
        current_user = request.current_user

        exist_payment = Payment.objects.filter(order_id = req['order_id'], deleted = 0)
        if exist_payment:
            return False

        payment = {
            'first_name': current_user['first_name'],
            'last_name': current_user['last_name'],
            'mobile': current_user['mobile'],
            'order_id': req['order_id'],
            'total': req['total'],
            'method': req['method'],
            'status': status
        }
        Payment.objects.create(**payment)

        return True
    except:
        return False


@verify_token
@api_view(['POST'])
def confirm_payment(request):
    try:
        result = create_payment(request, PAYMENT_STATUS['DONE'])
        if not result:
            return response_error('Bad Request', http_status.HTTP_400_BAD_REQUEST)
        return response_success('Paid Successfully', http_status.HTTP_201_CREATED)
    except:
        return response_error('Bad Request', http_status.HTTP_400_BAD_REQUEST)


@verify_token
@api_view(['POST'])
def create(request):
    try:
        result = create_payment(request, PAYMENT_STATUS['PENDING'])
        if not result:
            return response_error('Bad Request', http_status.HTTP_400_BAD_REQUEST)
        return response_success('Created Successfully', http_status.HTTP_201_CREATED)
    except:
        return response_error('Bad Request', http_status.HTTP_400_BAD_REQUEST)


@verify_token
@api_view(['GET'])
def get_my_order_payment(request, order_id):
    try:
        my_order_payment = Payment.objects.get(order_id = order_id, deleted = 0)

        return response_success('', PaymentSerializer(my_order_payment, many = True).data)
    except ObjectDoesNotExist:
        return response_error('Payment does not exist', http_status.HTTP_404_NOT_FOUND)
    except:
        return response_error('Bad Request', http_status.HTTP_400_BAD_REQUEST)


@verify_token
@check_permission
@api_view(['GET'])
def get_all_payments(request):
    q = request.GET.get('q')
    page_query = request.GET.get('page')
    sort_order = request.GET.get('sort_order')
    field = request.GET.get('field')
    status = request.GET.get('status')

    if sort_order and field:
        field = '-' + field if sort_order == 'desc' else field
    else:
        field = '-created_at'

    page = int(page_query) if page_query is not None else 1
    from_page = PER_PAGE * (page - 1)
    to_page = PER_PAGE

    payments = Payment.objects.filter(deleted = 0).order_by(field)

    if q is not None:
        search = q.strip()
        payments = payments.filter(
            Q(pk = search) |
            Q(first_name__icontains = search) |
            Q(last_name__icontains = search)
        )

    if status is not None:
        payments = payments.filter(status = status)

    payments = payments[from_page:to_page]

    response_data = {
        'page': page,
        'per_page': PER_PAGE,
        'total': len(payments),
        'payments': PaymentSerializer(payments, many = True).data
    }

    return response_success('Success', response_data)


@verify_token
@check_permission
@api_view(['PATCH'])
def update_status(request, id):
    try:
        new_status = json.loads(request.body)['status']
        if new_status not in PAYMENT_STATUS.values():
            return response_error(f"Order status must be in {PAYMENT_STATUS.values()}")

        payment = Payment.objects.get(pk = id, deleted = 0)
        payment.status = new_status
        payment.save()

        return response_success('Updated Successfully')
    except ObjectDoesNotExist:
        return response_error('Payment does not exist', http_status.HTTP_404_NOT_FOUND)
    except:
        return response_error('Bad Request', http_status.HTTP_400_BAD_REQUEST)
