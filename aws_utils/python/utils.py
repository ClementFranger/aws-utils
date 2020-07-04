import logging
import decimal
import json
from functools import wraps

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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


# def aws_output(*args, **kwargs):
#     def decorator(f):
#         @wraps(f)
#         def wrapper(self):
#             response = f(self, *args, **kwargs)
#             # response = response if isinstance(response, str) else str(response)
#             # TODO : ADD CLIENT DOMAIN WHEN IN PRODUCTION
#             return {"statusCode": kwargs.get('status_code', 200),
#                     "headers": kwargs.get('headers'),
#                     "body": json.dumps(response, cls=DecimalEncoder)}
#         return wrapper
#     return decorator


def validate_request(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        kwargs.update({k: v if v is not None else dict() for k, v in kwargs.items()})
        # [v if v is not None else dict() for v in kwargs.values()]
        return f(*args, **kwargs)
    return wrapper


def load_payload(f):
    @wraps(f)
    def wrapper(event, *args, **kwargs):
        logger.info('event : {event}'.format(event=event))
        print(type(event.get('pathParameters')))
        try:
            body, path, query = [json.loads(p) if p else dict() for p in
                                 [event.get('body'), event.get('pathParameters'), event.get('queryStringParameters')]]
            kwargs.update({'body': body, 'path': path, 'query': query})

            print(kwargs)
        except TypeError as e:
            raise TypeError('Error when parsing body : {e}'.format(e=e))
        return f(event, *args, **kwargs)
    return wrapper


def check_payload(id):
    def decorator(event):
        @wraps(event)
        def wrapper(*args, **kwargs):
            if kwargs.get('body') and not kwargs.get('body').get(id):
                return failure(code=400, body='You should provide a {id} key to your body'.format(id=id))
            if kwargs.get('path') and not kwargs.get('path').get(id):
                return failure(code=400, body='You should provide a {id} key to your pathParameters'.format(id=id))
            return event(*args, **kwargs)
        return wrapper
    return decorator


def validate_params(**kwargs):
    return [v if v is not None else dict() for v in kwargs.values()]


def success(**kwargs):
    # body = kwargs.get('body') if isinstance(kwargs.get('body'), str) else str(kwargs.get('body'))
    # TODO : ADD CLIENT DOMAIN WHEN IN PRODUCTION
    return {"statusCode": kwargs.get('status_code', 200), "headers": kwargs.get('headers'), "body": json.dumps(kwargs.get('body'), cls=DecimalEncoder)}


def failure(**kwargs):
    # body = kwargs.get('body') if isinstance(kwargs.get('body'), str) else str(kwargs.get('body'))
    return {"statusCode": kwargs.get('status_code', 500), "body": kwargs.get('body')}
