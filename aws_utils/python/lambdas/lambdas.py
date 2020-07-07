import json
import logging
from functools import wraps

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Lambdas(object):

    class Decorators(object):
        @classmethod
        def output(cls, f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                result = f(*args, **kwargs)
                return {'statusCode': result.get('ResponseMetadata').get('HTTPStatusCode'), 'body': result}
            return wrapper

        @classmethod
        def payload(cls, id='id'):
            def decorator(f):
                @wraps(f)
                def wrapper(event, *args, **kwargs):
                    logger.info('Received payload : {payload}'.format(payload=event.get('body')))

                    body = json.loads(event.get('body')) if event.get('body') else dict()

                    if body and not body.get(id):
                        return 400, 'You should provide a {id} key to your body'.format(id=id)
                    if event.get('pathParameters') and not event.get('pathParameters').get(id):
                        return 400, 'You should provide a {id} key to your pathParameters'.format(id=id)
                    kwargs.update({'body': body, 'path': event.get('pathParameters'),
                                   'query': event.get('queryStringParameters')})

                    logger.info('Payload have been loaded into kwargs : {kwargs}'.format(kwargs=kwargs))
                    return f(event, *args, **kwargs)
                return wrapper
            return decorator
