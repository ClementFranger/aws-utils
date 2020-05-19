import json
import logging
import boto3

from utils import DecimalEncoder, success, failure, validate_params

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.resource('dynamodb')


def scan(event, context, **kwargs):
    logger.info('event : {event}'.format(event=event))
    # path, = validate_params(path=event.get('pathParameters'))

    # id = path.get('id')
    # if not id:
    #     return failure(code=400, body='You should provide a id to your path parameters')

    params = {
        'TableName': kwargs.get('table')
    }

    if kwargs.get('filter'):
        params.update({'FilterExpression': kwargs.get('filter')})

    logger.info('Getting all items')

    try:
        result = client.Table(params.get('TableName')).scan(**params)
        if not result.get('Items'):
            return success(status_code=204, body=json.dumps(result.get('Items'), cls=DecimalEncoder))
    except Exception as e:
        return failure(body=e)

    logger.info('Retrieved all items')
    return success(body=json.dumps(result.get('Items'), cls=DecimalEncoder))
