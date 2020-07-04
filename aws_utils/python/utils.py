import decimal
import json
from functools import wraps


class DecimalEncoder(json.JSONEncoder):
    """ makes json serialize decimal (for boto3) """

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def handle_request(request):
    @wraps(request)
    def wrapper(self, *args, **kwargs):
        try:
            response = request(self, *args, **kwargs)
        except Exception as e:
            return failure(body=e)
        return response
    return wrapper


def output_request(request):
    @wraps(request)
    def wrapper(self, *args, **kwargs):
        response = request(self, *args, **kwargs)
        try:
            response = response.json()
        except Exception as e:
            return failure(body=e)
        return response
    return wrapper


def validate_request(request):
    @wraps(request)
    def wrapper(*args, **kwargs):
        kwargs.update({k: v if v is not None else dict() for k, v in kwargs.items()})
        # [v if v is not None else dict() for v in kwargs.values()]
        return request(*args, **kwargs)
    return wrapper


def load_body(f):
    @wraps(f)
    def wrapper(event, *args, **kwargs):
        try:
            body = json.loads(event.get('body'))
            kwargs.update({'body': body})
        except TypeError as e:
            return failure(body='Error when parsing body : {e}'.format(e=e))
        return f(event, *args, **kwargs)
    return wrapper


def check_body_id(id):
    def decorator(event):
        @wraps(event)
        def wrapper(*args, **kwargs):
            if not kwargs.get('body').get(id):
                return failure(code=400, body='You should provide a {id} key to your body'.format(id=id))
            return event(*args, **kwargs)
        return wrapper
    return decorator


def validate_params(**kwargs):
    return [v if v is not None else dict() for v in kwargs.values()]


def success(**kwargs):
    status_code = kwargs.get('status_code', 200)
    # TODO : ADD CLIENT DOMAIN WHEN IN PRODUCTION
    headers = kwargs.get('headers', {'Access-Control-Allow-Origin': '*'})
    body = kwargs.get('body') if isinstance(kwargs.get('body'), str) else str(kwargs.get('body'))
    return {"statusCode": status_code, "headers": headers, "body": body}


def failure(**kwargs):
    status_code = kwargs.get('status_code', 500)
    body = kwargs.get('body') if isinstance(kwargs.get('body'), str) else str(kwargs.get('body'))
    return {"statusCode": status_code, "body": body}
