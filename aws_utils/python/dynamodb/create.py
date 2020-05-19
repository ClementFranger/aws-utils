import json
import logging
import boto3
from utils import DecimalEncoder, success, failure

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.resource('dynamodb')


def create(**kwargs):
    key, params = kwargs.get('key'), kwargs.get('params')

    logger.info('Creating item {key}'.format(key=key))

    try:
        client.Table(params.get('TableName')).put_item(**params)
    except Exception as e:
        return failure(body=e)

    logger.info('Created item {key}'.format(key=key))
    return success(body=json.dumps(params['Item'], cls=DecimalEncoder))
