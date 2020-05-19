import json
import logging
import boto3
from utils import DecimalEncoder, success, failure, validate_params

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.resource('dynamodb')


def get(event, context, **kwargs):
    # logger.info('event : {event}'.format(event=event))
    # path, = validate_params(path=event.get('pathParameters'))
    #
    # id = path.get('id')
    # if not id:
    #     return failure(code=400, body='You should provide a id to your path parameters')
    #
    # params = {
    #     'TableName': table,
    #     'Key': {'id': id}
    # }
    key, params = kwargs.get('key'), kwargs.get('params')

    logger.info('Getting item {key}'.format(key=key))

    try:
        result = client.Table(params.get('TableName')).get_item(**params)
        if not result.get('Item'):
            return success(status_code=204, body=json.dumps(result.get('Item'), cls=DecimalEncoder))
    except Exception as e:
        return failure(body=e)

    logger.info('Retrieved item {key}'.format(key=key))
    return success(body=json.dumps(result.get('Item'), cls=DecimalEncoder))
