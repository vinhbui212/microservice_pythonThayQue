from constants import MAX_STRING_LENGTH
from model.models import PAYMENT_METHOD

create_and_update_schema = {
    'user_id': {},
    'total': {},
    'status': {},
    'payment_status': {},
    'payment_method': {
        'type': 'integer',
        'required': True,
        'allowed': PAYMENT_METHOD.values()
    },
    'shipping_address': {
        'type': 'string',
        'required': True,
        'minlength': 1,
        'maxlength': MAX_STRING_LENGTH
    }
}
