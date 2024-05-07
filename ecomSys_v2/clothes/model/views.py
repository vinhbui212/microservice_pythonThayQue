import re
from bson import ObjectId
from django.db.models import Q
from rest_framework.decorators import api_view
from clothes.decorators import verify_token, check_permission
from category.models import Category
from constants import PER_PAGE
from helpers import response_success, handle_query, response_error
from model.models import Clothes, CLOTHES_STATUS
from model.requests import create_and_update_schema
from model.serializers import ClothesSerializer
from model.validator import ClothesValidator
from rest_framework import status as http_status
from ast import literal_eval


# Create your views here.

@verify_token
@api_view(['GET'])
def clothes(request):
    queries = handle_query(request)

    if queries['category_id'] is not None:
        if not ObjectId.is_valid(queries['category_id']):
            return response_error('Category ID must be an ObjectId.')

        exist_category = Category.objects.filter(_id = ObjectId(queries['category_id']), deleted = 0)
        if not exist_category:
            return response_error('Category does not exist.')

    clothes_list = (Clothes.objects
                    .filter(deleted = 0, status = CLOTHES_STATUS['AVAILABLE'])
                    .order_by(queries['field']))

    if queries['q'] is not None:
        clothes_list = clothes_list.filter(
            Q(name__icontains = queries['q'].strip()) |
            Q(code__icontains = queries['q'].strip())
        )

    if queries['category_id'] is not None:
        clothes_list = clothes_list.filter(categories___id = ObjectId(queries['category_id']))

    clothes_list = clothes_list[queries['from_page']:queries['to_page']]

    return response_success('Success', ClothesSerializer(clothes_list, many = True).data)


@verify_token
@check_permission
@api_view(['GET'])
def admin_get_clothes(request):
    queries = handle_query(request)
    clothes_list = Clothes.objects.filter(deleted = 0).order_by(queries['field'])

    if queries['q'] is not None:
        q = queries['q'].strip()
        clothes_list = clothes_list.filter(Q(name__icontains = q) | Q(code__icontains = q))

    clothes_list = clothes_list[queries['from_page']:queries['to_page']]

    response_data = {
        'page': queries['page'],
        'per_page': PER_PAGE,
        'total': len(clothes_list),
        'mobiles': ClothesSerializer(clothes_list, many = True).data
    }

    return response_success('Success', response_data)


@verify_token
@check_permission
@api_view(['POST'])
def create(request):
    (name, description, price,
     old_price, status, quantity, category_ids, image) = prepare_request(request)

    clothes = {
        'code': create_new_code(),
        'name': name,
        'description': description,
        'price': int(price),
        'old_price': int(old_price) if old_price is not None else None,
        'status': int(status),
        'quantity': int(quantity),
        'image': image,
    }

    validator = ClothesValidator(create_and_update_schema)
    if validator.validate(clothes):
        try:
            new_clothes = Clothes.objects.create(**clothes)
            category_ids = [ObjectId(category_id) for category_id in literal_eval(category_ids)]
            categories = Category.objects.filter(_id__in = category_ids, deleted = 0)
            new_clothes.categories.set(categories)

            return response_success('Created successfully')
        except Exception as e:
            return response_error('Error', http_status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response_error('Error', http_status.HTTP_400_BAD_REQUEST, validator.errors)


@verify_token
@check_permission
@api_view(['PUT'])
def update(request, id):
    # validate
    if not ObjectId.is_valid(id):
        return response_error('Clothes ID must be an ObjectId.', http_status.HTTP_400_BAD_REQUEST)

    clothes = Clothes.objects.filter(_id = ObjectId(id), deleted = 0)
    if not clothes:
        return response_error('Clothes does not exist.', http_status.HTTP_400_BAD_REQUEST)

    clothes = clothes[0]
    (name, description, price,
     old_price, status, quantity, category_ids, image) = prepare_request(request)

    update_clothes = {
        'code': clothes.code,
        'name': name,
        'description': description,
        'price': int(price),
        'old_price': int(old_price) if old_price is not None else None,
        'status': int(status),
        'quantity': int(quantity),
        'image': image,
    }

    validator = ClothesValidator(create_and_update_schema)
    if validator.validate(update_clothes):
        try:
            clothes.name = name
            clothes.description = description
            clothes.price = price
            clothes.old_price = old_price
            clothes.status = status
            clothes.quantity = quantity
            clothes.category_ids = category_ids
            clothes.image = image
            clothes.save()

            category_ids = [ObjectId(category_id) for category_id in literal_eval(category_ids)]
            categories = Category.objects.filter(_id__in = category_ids, deleted = 0)
            clothes.categories.set(categories)

            return response_success('Updated successfully')
        except Exception as e:
            return response_error('Error', http_status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response_error('Error', http_status.HTTP_400_BAD_REQUEST, validator.errors)


@verify_token
@check_permission
@api_view(['DELETE'])
def delete(request, id):
    # validate
    if not ObjectId.is_valid(id):
        return response_error('Clothes ID must be an ObjectId.', http_status.HTTP_400_BAD_REQUEST)

    clothes = Clothes.objects.filter(_id = ObjectId(id), deleted = 0)
    if not clothes:
        return response_error('Clothes does not exist.', http_status.HTTP_400_BAD_REQUEST)

    clothes = clothes[0]
    clothes.deleted = 1
    clothes.save()
    clothes.categories.clear()

    return response_success('Deleted Successfully')


def create_new_code():
    latest_clothes = Clothes.objects.all().order_by('-created_at').first()
    latest_code_number = int(re.findall(r'\d+', latest_clothes.code)[0]) if latest_clothes is not None else -1
    return 'CL' + str(latest_code_number + 1)


def prepare_request(request):
    req = request.POST

    return [
        req.get("name"),
        req.get("description"),
        req.get("price"),
        req.get("old_price"),
        req.get("status"),
        req.get("quantity"),
        req.get("category_ids"),
        request.FILES.get("image")
    ]
