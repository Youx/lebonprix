import requests
import json
from datetime import datetime
from lebonprix.cache import Cache


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
    def __init__(self, item_id, session, additional_info=None):
        self.id = item_id
        self.session = session
        self.additional_info = additional_info if additional_info else {}
        self.cache = Cache()

    def in_cache(self):
        if self.cache.get(self.id) is not None:
            return True
        return False

    def __call__(self):
        cached_item = self.cache.get(self.id)
        if cached_item is not None:
            # upgrade database if needed
            need_to_update = False
            for key in self.additional_info:
                if key not in cached_item:
                    need_to_update = True
                    #cached_item[key] = self.additional_info[key]
            if need_to_update:
                self.cache.set({**cached_item, **self.additional_info})
                return {**cached_item, **self.additional_info}
            return cached_item

        r = self.session.post(
            url = self.BASE_URI + self.PAGE,
            params = {'ad_id': self.id},
            data = {**self.DATA, **{'ad_id': self.id}}, # copy data
            headers = self.HEADERS
        )
        item = {
            **json.loads(r.text),
            **self.additional_info
        }
        self.cache.set(item)
        return item


class Search(LBC):
    PAGE = 'list.json'

    def __init__(self, search_limit, default_params, additional_params=None):
        additional_params = [] if additional_params is None else additional_params
        self.list = None
        self.search_limit = search_limit
        self.session = requests.Session()
        self.params = default_params.copy()
        for param in additional_params:
            self.params.update(param.as_param())

    @staticmethod
    def pivot_from_item(item):
        try:
            price = int(item['price'].replace(' ', ''))
        except:
            price=0
        return '{},{},{}'.format(
            item['list_id'],
            int(datetime.strptime(item['list_time'], '%Y-%m-%d %H:%M:%S').timestamp()),
            price
        )

    def __call__(self):
        fetch_count = 0
        current_page = 1
        last_page = -1
        pivot = '0,0,0'
        while last_page == -1 or current_page <= last_page:
            l = self.get_list(pivot)
            if last_page == -1:
                last_page = int(l['lastpagenumber'].replace(' ', ''))
            for x in l['ads']:
                item = Item(x['list_id'], self.session, {'thumb': x.get('thumb', '')})
                if item.in_cache():
                    yield item
                elif self.search_limit == -1:
                    yield item
                elif fetch_count < self.search_limit:
                    fetch_count += 1
                    yield item
                else:
                    break
            if self.search_limit != -1 and fetch_count >= self.search_limit:
                break
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
