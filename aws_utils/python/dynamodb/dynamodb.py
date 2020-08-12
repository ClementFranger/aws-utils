import logging
import boto3


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DynamoDB(object):
    _TABLE_NAME = None
    __CLIENT__ = boto3.resource('dynamodb')

    def __init__(self, **kwargs):
        self.__TABLE__ = self.__CLIENT__.Table(kwargs.get('_TABLE_NAME', self._TABLE_NAME))

    def scan(self, **kwargs):
        result = self.__TABLE__.scan()
        logger.info('Retrieved {count} items from {table} table'.format(count=result.get('Count'), table=self._TABLE_NAME))
        return result

    def put(self, **kwargs):
        result = self.__TABLE__.put_item(**kwargs)
        logger.info('Created item {item} to {table} table'.format(item=kwargs.get('Item'), table=self._TABLE_NAME))
        return result

    def get(self, **kwargs):
        result = self.__TABLE__.get_item(**kwargs)
        logger.info('Retrieved item {key} from {table} table'.format(key=kwargs.get('Key'), table=self._TABLE_NAME))
        return result

    def batch_put(self, **kwargs):
        logger.info('Creating batch')
        with self.__TABLE__.batch_writer() as batch:
            [batch.put_item(Item=item) for item in kwargs.get('Items')]

        logger.info('Created batch')
