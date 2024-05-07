import requests
from django.http import HttpResponse
import json
from requests import HTTPError, Timeout


def response_success(message = '', data = None, status_code = 200):
    if data is None:
        data = {}

    return HttpResponse(json.dumps({
        'status': 'Success',
        'status_code': status_code,
        'message': message,
        'data': data
    }), content_type = 'application/json')


def response_error(message = '', status_code = 400, error = None):
    if error is None:
        error = {}

    return HttpResponse(json.dumps({
        'status': 'Failed',
        'status_code': status_code,
        'message': message,
        'error': error
    }), content_type = 'application/json')


def call_api(request, url, params = None):
    if params is None:
        params = {}
    try:
        url = url
        header = {
            "Content-Type": "application/json",
            "Authorization": request.META.get('HTTP_AUTHORIZATION', '')
        }

        result = requests.get(url, headers = header, params = params)
        result.raise_for_status()

        if result.json()['status'] == 'Success':
            return result.json()
        return response_error(result.json()['message'], result.json()['status_code'])

    except HTTPError as http_err:
        response_error(f"HTTP error occurred: {http_err}")
    except Timeout:
        response_error("The request timed out")
    except ConnectionError:
        response_error("Network connection error")
    except Exception as err:
        response_error(f"An error occurred: {err}")
