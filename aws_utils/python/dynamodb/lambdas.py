from lambdas.lambdas import Lambdas
from dynamodb.dynamodb import DynamoDB


class LambdasDynamoDB(Lambdas):
    __DYNAMODB_TABLE__ = None

    def __init__(self, **kwargs):
        self.__DYNAMODB__ = DynamoDB(__DYNAMODB_TABLE__=self.__DYNAMODB_TABLE__, **kwargs)

    @Lambdas.Decorators.output
    def scan(self, *args, **kwargs):
        return self.__DYNAMODB__.scan()

    @Lambdas.Decorators.output
    @Lambdas.Decorators.payload(id='_id')
    def get(self, *args, **kwargs):
        return self.__DYNAMODB__.get(Key=kwargs.get('path'))

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Lambdas.Decorators.output
    @Lambdas.Decorators.payload(id='_id')
    def put(self, *args, **kwargs):
        print('salut')
        return self.__DYNAMODB__.put(Item=kwargs.get('body'))

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Lambdas.Decorators.payload(id=None, load=False)
    def batch_put(self, *args, **kwargs):
        return self.__DYNAMODB__.batch_put(Items=kwargs.get('body'))
