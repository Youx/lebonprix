from lebonprix.crawler.search import Search
import numpy as np
from lebonprix.lr import LinearRegression


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
        return {'it': 1, 'q': self.val}


class CarParamModel:
    MODELS = {
        'Toyota': ['Gt86'],
        'Peugeot': ['207'],
    }
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

    def prepare_input(self, search_results):
        def transform_gearbox(val):
            return 1 if val == 'Manuelle' else 0
        def transform_mileage(val):
            return int(val.rstrip(' KM').replace(' ', ''))
        def transform_price(val):
            return int(val.replace(' ', ''))
        def transform_regdate(val):
            return int(val)
        def transform_company_ad(val):
            return int(val)

        res = []
        for search_result in search_results:
            row = {}
            row['price'] = transform_price(search_result['price'])
            row['company_ad'] = transform_company_ad(search_result['company_ad'])
            row['gearbox'] = [ transform_gearbox(param['value'])
                               for param in search_result['parameters']
                               if param['id'] == 'gearbox' ][0]
            row['mileage'] = [ transform_mileage(param['value'])
                               for param in search_result['parameters']
                               if param['id'] == 'mileage' ][0]
            row['regdate'] = [ transform_regdate(param['value'])
                               for param in search_result['parameters']
                               if param['id'] == 'regdate' ][0]
            res.append(row)
        return res
            
    def search(self, brand, model, fuel):
        params = [
            CarParamModel(brand, model),
            CarParamFuel(fuel),
            CarParamCategory(),
        ]
        lst = super().search(self.DEFAULT_PARAMS, params)
        #lst = super().search(self.URI, None)
        res = []
        for x in lst['ads']:
            res.append(super().item(x['list_id']))
        return res
    
    def predict(self, prepared_inputs, guess):
        lr = LinearRegression()
        guess_prep = np.array([[float(guess['gearbox']),
                                float(guess['mileage']),
                                float(guess['regdate']),
                                float(guess['company_ad'])]])
        x, y = lr.prepare_input(prepared_inputs, ['gearbox', 'mileage', 'regdate', 'company_ad'], 'price')
        return lr.lr(x, y, guess_prep)
