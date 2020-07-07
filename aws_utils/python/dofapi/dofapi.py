from functools import wraps

import requests
import logging
from utils import to_json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Dofapi(object):
    __DOFAPI_API_ = 'https://fr.dofus.dofapi.fr/'
    __WEAPONS__ = 'weapons'

    class Decorators(object):
        @classmethod
        def output(cls, f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs).json()
            return wrapper

    @Decorators.output
    def scan_weapons(self, *args, **kwargs):
        logger.info('Getting all weapons')

        result = requests.get(self.__DOFAPI_API_ + self.__WEAPONS__, *args, **kwargs)

        logger.info('Retrieved all weapons')
        return result
