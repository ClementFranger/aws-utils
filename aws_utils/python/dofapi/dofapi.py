from functools import wraps

import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
        endpoint, unique = kwargs.get('endpoint', self.__RESOURCES__), kwargs.get('unique', False)

        logger.info('Getting all {endpoint}'.format(endpoint=endpoint))

        result = requests.get(self.__DOFAPI_API_ + endpoint, *args)

        logger.info('Retrieved {endpoint}'.format(endpoint=endpoint))
        return list({v[self.__ID__]: v for v in result}.values()) if unique else result

    @Decorators.output
    def scan_consumables(self, *args, **kwargs):
        return self._scan(endpoint=self.__CONSUMABLES__, *args, **kwargs)

    @Decorators.output
    def scan_equipments(self, *args, **kwargs):
        return self._scan(endpoint=self.__EQUIPMENTS__, *args, **kwargs)

    @Decorators.output
    def scan_idols(self, *args, **kwargs):
        return self._scan(endpoint=self.__IDOLS__, *args, **kwargs)

    @Decorators.output
    def scan_resources(self, *args, **kwargs):
        return self._scan(endpoint=self.__RESOURCES__, *args, **kwargs)

    @Decorators.output
    def scan_weapons(self, *args, **kwargs):
        return self._scan(endpoint=self.__WEAPONS__, *args, **kwargs)

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
