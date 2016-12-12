import requests
import json
from datetime import datetime


class LBC:
    BASE_URI = 'https://mobile.leboncoin.fr/templates/api/'
    DATA = {
        'app_id': 'leboncoin_iphone',
        'key': ('c17d5009f2de512fae68880ea4375ef8adbc3'
                '4e56a7444c0248fcb63bd0ffaed9995200a46'
                'cee0176654b244c9b9f2934d935576650b15c'
                '6792621e94cbec163')
    }
    HEADERS = {'User-Agent': 'Leboncoin/3.15.2 (iPhone; iOS 9.3.1; Scale/2.00)'}


class Item(LBC):
    PAGE = 'view.json'
    def __init__(self, item_id, session):
        self.id = item_id
        self.session = session

    def __call__(self):
        new_data = self.DATA.copy()
        new_data['ad_id'] = self.id
        r = self.session.post(
            url = self.BASE_URI + self.PAGE,
            params = {'ad_id': self.id},
            data = new_data,
            headers = self.HEADERS
        )
        return json.loads(r.text)


class Search(LBC):
    PAGE = 'list.json'

    def __init__(self, default_params, additional_params=None):
        self.list = None
        self.session = requests.Session()
        self.params = default_params.copy()
        for param in additional_params:
            self.params.update(param.as_param())
    
    @staticmethod
    def pivot_from_item(item):
        return '{},{},{}'.format(
            item['list_id'],
            int(datetime.strptime(item['list_time'], '%Y-%m-%d %H:%M:%S').timestamp()),
            int(item['price'].replace(' ', ''))
        )

    def __call__(self):
        current_page = 1
        last_page = -1
        pivot = '0,0,0'
        while last_page == -1 or current_page <= last_page:
            l = self.get_list(pivot)
            if last_page == -1:
                last_page = int(l['lastpagenumber'].replace(' ', ''))
            for x in l['ads']:
                yield Item(x['list_id'], self.session)
            # update pivot to get next page
            pivot = self.pivot_from_item(l['ads'][-1])
            current_page += 1

    def get_list(self, pivot):
        r = self.session.post(
            url = self.BASE_URI + Search.PAGE + '?pivot={}'.format(pivot),
            data = self.DATA,
            params = self.params,
            headers = self.HEADERS,
        )
        return json.loads(r.text)
