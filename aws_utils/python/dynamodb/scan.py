import json
import logging
from functools import reduce

import boto3
from boto3.dynamodb.conditions import Attr

from utils import DecimalEncoder, success, failure, validate_params

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.resource('dynamodb')


def scan(event, context, **kwargs):
    # logger.info('event : {event}'.format(event=event))
    # body, = validate_params(body=event.get('body'))
    #
    # body = json.loads(body) if isinstance(body, str) else body
    #
    # params = {'TableName': kwargs.get('table')}
    #
    # if body and body.get('filter'):
    #     params.update({'FilterExpression': reduce(lambda a, b: a & b, [Attr(k).eq(v) for k, v in body.get('filter').items])})
    params = kwargs.get('params')

    logger.info('Getting all items')

    try:
        result = client.Table(params.get('TableName')).scan(**params)
        if not result.get('Items'):
            return success(status_code=204, body=json.dumps(result.get('Items'), cls=DecimalEncoder))
    except Exception as e:
        return failure(body=e)

    logger.info('Retrieved all items')
    return success(body=json.dumps(result.get('Items'), cls=DecimalEncoder))
