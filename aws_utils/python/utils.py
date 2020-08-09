import logging
import decimal
import json
import re
from functools import wraps

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# TODO : put in class to make return int changeable
class DecimalEncoder(json.JSONEncoder):
    """ makes json serialize decimal (for boto3) """

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return int(o)
        return super(DecimalEncoder, self).default(o)


class Schema(object):

    @classmethod
    def keys(cls):
        return [k for k in vars(cls) if not k.startswith('__')]

    @classmethod
    def values(cls):
        return [getattr(cls, k) for k in cls.keys()]


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


def load_payload(f):
    @wraps(f)
    def wrapper(self, event, *args, **kwargs):
        try:
            body = json.loads(event.get('body')) if event.get('body') else dict()
            kwargs.update(
                {'body': body, 'path': event.get('pathParameters'), 'query': event.get('queryStringParameters')})
        except TypeError as e:
            raise TypeError('Error when parsing body : {e}'.format(e=e))
        return f(self, event, *args, **kwargs)
    return wrapper


def check_payload(id):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if kwargs.get('body') and not kwargs.get('body').get(id):
                return failure(code=400, body='You should provide a {id} key to your body'.format(id=id))
            if kwargs.get('path') and not kwargs.get('path').get(id):
                return failure(code=400, body='You should provide a {id} key to your pathParameters'.format(id=id))
            return f(*args, **kwargs)
        return wrapper
    return decorator


def cors(ips):
    def decorator(f):
        @wraps(f)
        def wrapper(event, context, *args, **kwargs):
            logger.info('event : {event}'.format(event=event))
            if any(re.compile(ip).match(event.get('headers').get('origin')) for ip in ips):
                kwargs.update({'headers': {'Access-Control-Allow-Origin': event.get('headers').get('origin')}})
            return f(event, context, *args, **kwargs)
        return wrapper
    return decorator


def success(**kwargs):
    return {"statusCode": kwargs.get('status_code', 200), "headers": kwargs.get('headers'),
            "body": json.dumps(kwargs.get('body'), cls=DecimalEncoder)}


def failure(**kwargs):
    return {"statusCode": kwargs.get('status_code', 500), "body": kwargs.get('body')}
