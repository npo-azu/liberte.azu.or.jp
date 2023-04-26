#----------------------------------------------------------
# Import
#----------------------------------------------------------
# Standard library
import datetime
import urllib.parse
import logging

# Additional library
import requests

# Other module


#----------------------------------------------------------
# INIT
#----------------------------------------------------------
# Get logger
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


#----------------------------------------------------------
# INIT
#----------------------------------------------------------
class MicroCMS:
    def __init__(self, service_id, api_key):
        _logger.debug(f'Create instance. service_id={service_id}')
        self.__url = f'https://{service_id}.microcms.io/api/v1/'
        self.__key = api_key


    def __parse_content(self, content_obj):
        ret = dict()

        for key, value in content_obj.items():
            if type(value) is str:
                try:
                    replaced = value.replace('Z', '+00:00')
                    ret[key] = datetime.datetime.fromisoformat(replaced).astimezone()
                    continue
                except ValueError:
                    pass
            ret[key] = value
        return ret


    def get_item(self, api_name, id=None, draft_key=None):
        endpoint = urllib.parse.urljoin(self.__url, api_name)
        if id is not None:
            endpoint = urllib.parse.urljoin(endpoint + '/', id)
        _logger.debug(f'endpoing: {endpoint}')
        headers = {
            'X-MICROCMS-API-KEY': self.__key,
        }

        params = dict()
        if draft_key:
            params['draftKey'] = draft_key
        _logger.debug(f'params: {params}')

        res = requests.get(endpoint, headers=headers, params=params)
        if res.status_code == 404:
            return None
        res.raise_for_status()

        return self.__parse_content( res.json() )


    def get_list(self, api_name, limit=10, offset=0, fields=None, filters=None):
        endpoint = urllib.parse.urljoin(self.__url, api_name)
        _logger.debug(f'endpoint: {endpoint}')

        headers = {
            'X-MICROCMS-API-KEY': self.__key
        }
        _logger.debug(f'headers: {headers}')

        params = {
            'limit' : limit,
            'offset': offset,
        }
        if fields:
            params['fields'] = fields
        if filters:
            params['filters'] = filters
        _logger.debug(f'params: {params}')

        res = requests.get(endpoint, headers=headers, params=params)
        res.raise_for_status()

        return [ self.__parse_content(i) for i in res.json()['contents'] ]


    def add_item(self, api_name, params, id=None):
        endpoint = urllib.parse.urljoin(self.__url, api_name)
        _logger.debug(f'endpoing: {endpoint}')
        headers = {
            'X-MICROCMS-API-KEY': self.__key,
        }
        _logger.debug(f'params: {params}')

        if id is None:
            res = requests.post(endpoint, headers=headers, params=params)
        else:
            endpoint = urllib.parse.urljoin(f'{endpoint}/', id)
            res = requests.put(endpoint, headers=headers, json=params)

        _logger.debug(f'res: {res.text}')
        res.raise_for_status()

        return res.text


#----------------------------------------------------------
# for DEBUG
#----------------------------------------------------------
if __name__ == '__main__':
    pass
