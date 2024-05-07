from rest_framework.decorators import api_view

from constants import MODEL
from helpers import call_api, response_error, response_success
from search.decorators import verify_token, check_permission


# Create your views here.


@verify_token
@api_view(['GET'])
def search_by_key(request):
    q = request.GET.get("q")
    model_type = request.GET.get("model_type")
    params = {'q': q}

    result = None
    match int(model_type):
        case 0:
            result = call_api(request, "http://127.0.0.1:8001/books", params)
        case 1:
            result = call_api(request, "", params)
        case 2:
            result = call_api(request, "", params)
        case _:
            return response_error("Model type must be 0, 1 or 2 respectively represent for Book, Clothes, Mobile")

    return response_success('', result['data'])


@verify_token
@api_view(['GET'])
def search_by_voice(request):
    voice_key = request.GET.get("q")
    model_type = request.GET.get("model_type")
    params = {'q': voice_key}

    result = None
    match int(model_type):
        case 0:
            result = call_api(request, "http://127.0.0.1:8001/books", params)
        case 1:
            result = call_api(request, "", params)
        case 2:
            result = call_api(request, "", params)
        case _:
            return response_error("Model type must be 0, 1 or 2 respectively represent for Book, Clothes, Mobile")

    return response_success('', result['data'])


@verify_token
@check_permission
@api_view(['GET'])
def admin_search_by_key(request):
    q = request.GET.get("q")
    model_type = request.GET.get("model_type")
    params = {'q': q}

    result = None
    match int(model_type):
        case 0:
            result = call_api(request, "http://127.0.0.1:8001/book-list", params)
        case 1:
            result = call_api(request, "", params)
        case 2:
            result = call_api(request, "", params)
        case _:
            return response_error("Model type must be 0, 1 or 2 respectively represent for Book, Clothes, Mobile")

    return response_success('', result['data'])
