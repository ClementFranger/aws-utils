from functools import wraps

import requests
import requests_cache
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

requests_cache.install_cache('dofapi_cache', expire_after=60*60*24*7)


class Dofapi(object):
    __ID__ = '_id'
    __ANKAMA_ID__ = 'ankamaId'
    __NAME__ = 'name'

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

    def _scan(self, *args, **kwargs):
        endpoint = kwargs.get('endpoint', self.__RESOURCES__)

        logger.info('Getting all {endpoint}'.format(endpoint=endpoint))

        result = requests.get(self.__DOFAPI_API_ + endpoint, *args)

        logger.info('Retrieved {endpoint}'.format(endpoint=endpoint))
        return result

    @Decorators.output
    def scan_consumables(self, *args, **kwargs):
        # logger.info('Getting all consumables')
        #
        # result = requests.get(self.__DOFAPI_API_ + self.__CONSUMABLES__, *args, **kwargs)
        #
        # logger.info('Retrieved all consumables')
        return self._scan(endpoint=self.__CONSUMABLES__)

    @Decorators.output
    def scan_equipments(self, *args, **kwargs):
        # logger.info('Getting all equipments')
        #
        # result = requests.get(self.__DOFAPI_API_ + self.__EQUIPMENTS__, *args, **kwargs)
        #
        # logger.info('Retrieved all equipments')
        return self._scan(endpoint=self.__EQUIPMENTS__)

    @Decorators.output
    def scan_idols(self, *args, **kwargs):
        # logger.info('Getting all idols')
        #
        # result = requests.get(self.__DOFAPI_API_ + self.__IDOLS__, *args, **kwargs)
        #
        # logger.info('Retrieved all idols')
        return self._scan(endpoint=self.__IDOLS__)

    @Decorators.output
    def scan_resources(self, *args, **kwargs):
        # logger.info('Getting all resources')
        #
        # result = requests.get(self.__DOFAPI_API_ + self.__RESOURCES__, *args, **kwargs)
        #
        # logger.info('Retrieved all resources')
        return self._scan(endpoint=self.__RESOURCES__)

    @Decorators.output
    def scan_weapons(self, *args, **kwargs):
        # logger.info('Getting all weapons')
        #
        # result = requests.get(self.__DOFAPI_API_ + self.__WEAPONS__, *args, **kwargs)
        #
        # logger.info('Retrieved all weapons')
        return self._scan(endpoint=self.__WEAPONS__)

    def _scan_items(self, *args, **kwargs):
        unique = kwargs.get('unique', False)
        logger.info('Getting all items')

        result = []
        [result.extend(getattr(self, f)(*args, **kwargs)) for f in dir(self) if f.startswith('scan')]

        if unique:
            logger.info('length of NON UNIQUE items : %s' % len(result))
            result = list({v[self.__ID__]: v for v in result}.values())
            logger.info('length of UNIQUE items : %s' % len(result))

        logger.info('Retrieved all items')
        return result
