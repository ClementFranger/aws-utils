import json
import logging

import boto3

from utils import DecimalEncoder, success, failure

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.resource('dynamodb')


def scan(**kwargs):
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
