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


def load_payload(f):
    @wraps(f)
    def wrapper(event, *args, **kwargs):
        try:
            body = json.loads(event.get('body')) if event.get('body') else dict()
            kwargs.update({'body': body, 'path': event.get('pathParameters'), 'query': event.get('queryStringParameters')})
        except TypeError as e:
            raise TypeError('Error when parsing body : {e}'.format(e=e))
        return f(event, *args, **kwargs)
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
            if event.get('origin') in ips:
                kwargs.update({'headers': {'Access-Control-Allow-Origin': event.get('origin')}})
            print(kwargs)
            return f(event, context, *args, **kwargs)
        return wrapper
    return decorator


def success(**kwargs):
    return {"statusCode": kwargs.get('status_code', 200), "headers": kwargs.get('headers'), "body": json.dumps(kwargs.get('body'), cls=DecimalEncoder)}


def failure(**kwargs):
    return {"statusCode": kwargs.get('status_code', 500), "body": kwargs.get('body')}
