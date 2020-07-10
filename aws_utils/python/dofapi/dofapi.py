from functools import wraps

import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Dofapi(object):
    __ID__ = '_id'
    __ANKAMA_ID__ = 'ankamaId'

    __DOFAPI_API_ = 'https://fr.dofus.dofapi.fr/'
    __CONSUMABLES__ = 'consumables'
    __EQUIPMENTS__ = 'equipments'
    __IDOLS__ = 'idols'
    __RESOURCES__ = 'resources'
    __WEAPONS__ = 'weapons'

    class Decorators(object):
        @classmethod
        def output(cls, f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs).json()
            return wrapper

    @Decorators.output
    def scan_consumables(self, *args, **kwargs):
        logger.info('Getting all consumables')

        result = requests.get(self.__DOFAPI_API_ + self.__CONSUMABLES__, *args, **kwargs)

        logger.info('Retrieved all consumables')
        return result

    @Decorators.output
    def scan_equipments(self, *args, **kwargs):
        logger.info('Getting all equipments')

        result = requests.get(self.__DOFAPI_API_ + self.__EQUIPMENTS__, *args, **kwargs)

        logger.info('Retrieved all equipments')
        return result

    @Decorators.output
    def scan_idols(self, *args, **kwargs):
        logger.info('Getting all idols')

        result = requests.get(self.__DOFAPI_API_ + self.__IDOLS__, *args, **kwargs)

        logger.info('Retrieved all idols')
        return result

    @Decorators.output
    def scan_resources(self, *args, **kwargs):
        logger.info('Getting all resources')

        result = requests.get(self.__DOFAPI_API_ + self.__RESOURCES__, *args, **kwargs)

        logger.info('Retrieved all resources')
        return result

    @Decorators.output
    def scan_weapons(self, *args, **kwargs):
        logger.info('Getting all weapons')

        result = requests.get(self.__DOFAPI_API_ + self.__WEAPONS__, *args, **kwargs)

        logger.info('Retrieved all weapons')
        return result

    def _scan_items(self, *args, **kwargs):
        logger.info('Getting all items')

        result = []
        [result.extend(getattr(self, f)(*args, **kwargs)) for f in dir(self) if f.startswith('scan')]

        logger.info('Retrieved all items')
        return result
