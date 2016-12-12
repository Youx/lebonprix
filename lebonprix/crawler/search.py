import requests
import json


class Search:
    DATA = {
        'app_id': 'leboncoin_iphone',
        'key': ('c17d5009f2de512fae68880ea4375ef8adbc3'
                '4e56a7444c0248fcb63bd0ffaed9995200a46'
                'cee0176654b244c9b9f2934d935576650b15c'
                '6792621e94cbec163')
    }
    SEARCH_PAGE = 'list.json?pivot=0,0,0'
    ITEM_PAGE = 'view.json'
    HEADERS = {'User-Agent': 'Leboncoin/3.15.2 (iPhone; iOS 9.3.1; Scale/2.00)'}
    BASE_URI = 'https://mobile.leboncoin.fr/templates/api/'
    
    def search(self, default_params, additional_params=None):
        params = default_params.copy()
        for param in additional_params:
            params.update(param.as_param())

        r = requests.post(
            url = self.BASE_URI + self.SEARCH_PAGE,
            data = self.DATA,
            params = params,
            headers = self.HEADERS,
            #verify = False
        )
        return json.loads(r.text)
    
    def item(self, item_id):
        new_data = self.DATA.copy()
        new_data['ad_id'] = item_id
        r = requests.post(
            url = self.BASE_URI + self.ITEM_PAGE,
            params = {'ad_id': item_id},
            data = new_data,
            headers = self.HEADERS,
            #verify = False
        )
        return json.loads(r.text)
