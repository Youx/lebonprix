from lebonprix.crawler.search import Search, LBC
import numpy as np
import logging
import json
import html
from lebonprix.lr import LinearRegression
import requests


class CarBrandModel(LBC):
    PAGE = 'extdata.json'

    def __init__(self):
        self.models = self.fetch()

    def fetch(self):
        r = requests.post(
            url = self.BASE_URI + self.PAGE,
            data = self.DATA,
            headers = self.HEADERS
        )
        j = json.loads(r.text)['brand_model']
        return {**j['brand_top'], **j['brand_other']}


class CarParamFuel:
    VALUES = {
        'Essence': 1,
        'Diesel': 2,
        'GPL': 3,
        'Electrique': 4,
        'Autre': 5
    }
    def __init__(self, val):
        self.val = val

    def as_param(self):
        return {'fu': self.VALUES[self.val]}


class CarParamText:
    def __init__(self, val):
        self.val = val

    def as_param(self):
        return {'it': 1, 'q': self.val} if self.val is not None else {}


class CarParamModel:
    MODELS = CarBrandModel().models

    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def as_param(self):
        if self.brand in self.MODELS and self.model in self.MODELS[self.brand]:
            return {'brd': self.brand, 'mdl': self.model}
        else:
            return {}


class CarParamCategory:
    def as_param(self):
        return {'ca': '12_s'}


class CarSearch(Search):
    DEFAULT_PARAMS = {
        'o': 1,
        'w': 3,
        'sp': 0,
        'c': 2,
        'ur': 0,
        'f': 'a',
    }

    def __init__(self, brand, model, fuel, detail=None, search_limit=200):
        params = [
            CarParamModel(brand, model),
            CarParamFuel(fuel),
            CarParamCategory(),
            CarParamText(detail),
        ]
        super().__init__(search_limit=search_limit,
                         default_params=self.DEFAULT_PARAMS,
                         additional_params=params)

    def prepare_guess(self, item):
        def transform_gearbox(val):
            return 1.0 if val == 'Manuelle' else 0.0
        return [transform_gearbox(item['gearbox']), float(item['mileage']), float(item['regdate']), float(item['company_ad'])]

    @staticmethod
    def _transform_gearbox(val):
        return 1.0 if val == 'Manuelle' else 0.0

    def prepare_item(self, item):
        def transform_mileage(val):
            return float(val.rstrip(' KM').replace(' ', ''))
        def transform_price(val):
            return float(val.replace(' ', ''))
        def transform_regdate(val):
            return float(val)
        def transform_company_ad(val):
            return float(val)
        def transform_subject(val):
            return html.unescape(val)
        return {
            'id': item['list_id'],
            'subject': transform_subject(item['subject']),
            'thumb': item['thumb'],
            'price': transform_price(item['price']),
            'company_ad': transform_company_ad(item['company_ad']),
            'gearbox': [ self._transform_gearbox(param['value'])
                         for param in item['parameters']
                         if param['id'] == 'gearbox' ][0],
            'mileage': [ transform_mileage(param['value'])
                         for param in item['parameters']
                         if param['id'] == 'mileage' ][0],
            'regdate': [ transform_regdate(param['value'])
                         for param in item['parameters']
                         if param['id'] == 'regdate' ][0]
        }

    def print_car(self, car):
        print("{subject}, {mileage} KM, {price}€ (expected {expected_price}€) : https://www.leboncoin.fr/voitures/{id}.htm".format(**car))

    def __call__(self):
        for item in super().__call__():
            try:
                res = self.prepare_item(item())
            except KeyError:
                pass
            except json.decoder.JSONDecodeError:
                pass
            except ValueError:
                pass
            else:
                yield res

    def predict(self, inputs, guess):
        lr = LinearRegression()
        guess_prep = np.array([self.prepare_guess(guess)])
        x, y = lr.prepare_input(inputs, ['gearbox', 'mileage', 'regdate', 'company_ad'], 'price')
        return lr.lr(x, y, guess_prep)

    def find_best(self, inputs, count, filters=None):
        """ Find the N best car offers

        inputs []: the inputs returned by CarSearch()()
        count (int): the number of best offers to keep
        filters (dict): criterias to apply afterwards
            gearbox (str): 'Manuelle'/'Automatique'
            max_mileage (int): Max mileage in km
            max_price (int): Max price in €
        """
        filters = {} if filters is None else filters

        lr = LinearRegression()
        x, y = lr.prepare_input(inputs, ['gearbox', 'mileage', 'regdate', 'company_ad'], 'price')
        predicted_prices = lr.lr(x, y, x)
        for x in range(0, len(inputs)):
            inputs[x]['expected_price'] = int(predicted_prices[x])
            # compute % of how more expensive it is
            inputs[x]['economy_pc'] = int((float(inputs[x]['price']) / float(inputs[x]['expected_price']) - 1) * 100)

        sorted_inputs = sorted(inputs, key=lambda x: x['economy_pc'])
        filtered_inputs = sorted_inputs

        if 'gearbox' in filters:
            gearbox = self._transform_gearbox(filters['gearbox'])
            filtered_inputs = [x for x in filtered_inputs if x['gearbox'] == gearbox]

        if 'max_price' in filters:
            filtered_inputs = [x for x in filtered_inputs if x['price'] <= filters['max_price']]

        if 'max_mileage' in filters:
            filtered_inputs = [x for x in filtered_inputs if x['mileage'] <= filters['max_mileage']]

        return filtered_inputs[:count]