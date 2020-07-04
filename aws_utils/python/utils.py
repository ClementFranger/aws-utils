import decimal
import json
from functools import wraps


class DecimalEncoder(json.JSONEncoder):
    """ makes json serialize decimal (for boto3) """

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def request(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        try:
            response = f(self, *args, **kwargs)
        except Exception as e:
            raise e
        return response
    return wrapper


def to_json(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        response = f(self, *args, **kwargs)
        try:
            response = response.json()
        except TypeError as e:
            raise TypeError('Error when parsing response : {e}'.format(e=e))
        return response
    return wrapper


def aws_output(*args, **kwargs):
    def decorator(f):
        @wraps(f)
        def wrapper(self):
            response = f(self, *args, **kwargs)
            # response = response if isinstance(response, str) else str(response)
            # TODO : ADD CLIENT DOMAIN WHEN IN PRODUCTION
            return {"statusCode": kwargs.get('status_code', 200),
                    "headers": kwargs.get('headers'),
                    "body": json.dumps(response, cls=DecimalEncoder)}
        return wrapper
    return decorator


def validate_request(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        kwargs.update({k: v if v is not None else dict() for k, v in kwargs.items()})
        # [v if v is not None else dict() for v in kwargs.values()]
        return f(*args, **kwargs)
    return wrapper


def load_body(f):
    @wraps(f)
    def wrapper(event, *args, **kwargs):
        try:
            body = json.loads(event.get('body'))
            kwargs.update({'body': body})
        except TypeError as e:
            raise TypeError('Error when parsing body : {e}'.format(e=e))
        return f(event, *args, **kwargs)
    return wrapper


def check_body_id(id):
    def decorator(event):
        @wraps(event)
        def wrapper(*args, **kwargs):
            if not kwargs.get('body').get(id):
                # return failure(code=400, body='You should provide a {id} key to your body'.format(id=id))
                raise ValueError('You should provide a {id} key to your body'.format(id=id))
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
