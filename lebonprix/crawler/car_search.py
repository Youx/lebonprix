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
        return {'it': 1, 'q': self.val} if self.val is not None else {}


class CarParamModel:
    MODELS = {
        'Audi': ['100', '200', '80', '90', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A6/s6', 'A7', 'A8',
                 'Allroad', 'Coupe', 'Q3', 'Q5', 'Q7', 'R8', 'Rs3 Sportback', 'Rs4', 'Rs5',
                 'S4', 'S4 Avant', 'S4 Cabriolet', 'S5', 'S8', 'Tt', 'Tts', 'V8'],
        'Bmw': ['I3', 'I8', 'M3', 'M4', 'M5', 'M6',
                'Serie 1', 'Serie 2', 'Serie 3', 'Serie 4', 'Serie 5', 'Serie 6', 'Serie 7', 'Serie 8',
                'X1', 'X3', 'X4', 'X5', 'X6', 'Z1', 'Z-series'],
        'Toyota': ['Gt86'],
        'Peugeot': ['207', '208'],
        'Renault': ['Twingo'],
        'Dacia': ['Sandero'],
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

    def __init__(self, brand, model, fuel, detail=None):
        params = [
            CarParamModel(brand, model),
            CarParamFuel(fuel),
            CarParamCategory(),
            CarParamText(detail),
        ]
        super().__init__(self.DEFAULT_PARAMS, params)

    def prepare_guess(self, item):
        def transform_gearbox(val):
            return 1 if val == 'Manuelle' else 0
        return [transform_gearbox(item['gearbox']), item['mileage'], item['regdate'], item['company_ad']]

    def prepare_item(self, item):
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

        return {
            'price': transform_price(item['price']),
            'company_ad': transform_company_ad(item['company_ad']),
            'gearbox': [ transform_gearbox(param['value'])
                         for param in item['parameters']
                         if param['id'] == 'gearbox' ][0],
            'mileage': [ transform_mileage(param['value'])
                         for param in item['parameters']
                         if param['id'] == 'mileage' ][0],
            'regdate': [ transform_regdate(param['value'])
                         for param in item['parameters']
                         if param['id'] == 'regdate' ][0]
        }

    def __call__(self):
        for item in super().__call__():
            try:
                res = self.prepare_item(item())
            except:
                pass
            else:
                yield res
    
    def predict(self, inputs, guess):
        lr = LinearRegression()
        guess_prep = np.array([self.prepare_guess(guess)])
        x, y = lr.prepare_input(inputs, ['gearbox', 'mileage', 'regdate', 'company_ad'], 'price')
        return lr.lr(x, y, guess_prep)
