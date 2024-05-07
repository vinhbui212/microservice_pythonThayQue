from service.models import PRODUCT_TYPE, PRODUCT_STATUS

create_and_update_schema = {
    'product_id': {},
    'customer_id': {},
    'product_type': {
        'type': 'integer',
        'required': True,
        'allowed': PRODUCT_TYPE.values()
    },
    'quantity': {
        'type': 'integer',
        'required': True,
        'min': 1
    },
    'product_price': {
        'type': 'integer',
        'required': True
    },
    'product_status': {
        'type': 'integer',
        'required': True,
        'allowed': PRODUCT_STATUS.values()
    }
}
