#!/usr/bin/env python3

from lebonprix.crawler.car_search import CarSearch
import json


def predict_car_price(brand, model, fuel, gearbox, regdate, company_ad, mileage, spec=None):
    print("Expected price for {} {} {} {} {} from {} with {} km".format(
          brand, model, fuel, spec, gearbox, regdate, mileage
    ))
    s = CarSearch(brand=brand, model=model, fuel=fuel, detail=spec)
    data = list(s())
    print("Sample size : {} elements".format(len(data)))
    price = s.predict(data, {'gearbox': gearbox, 'regdate': regdate,
                             'company_ad': company_ad, 'mileage': mileage})
    print("Price : {}".format(int(price[0])))
    return price

def main():
    predict_car_price(brand='Peugeot', model='207', fuel='Essence', spec='vti 1.6',
                      gearbox='Manuelle', regdate='2007', company_ad=0, mileage= 110000)
    predict_car_price(brand='Toyota', model='Gt86', fuel='Essence',
                      gearbox='Manuelle', regdate='2012', company_ad=0, mileage= 40000)
    predict_car_price(brand='Renault', model='Twingo', fuel='Essence', spec='1.2',
                      gearbox='Manuelle', regdate='2000', company_ad=0, mileage=70000)
    predict_car_price(brand='Dacia', model='Sandero', fuel='Diesel', spec='1.5 laureate',
                      gearbox='Manuelle', regdate='2010', company_ad=0, mileage=103000)
    predict_car_price(brand='Peugeot', model='208', fuel='Diesel', spec='1.6 92 active',
                      gearbox='Manuelle', regdate='2015', company_ad=0, mileage=50000)


def main():
    s = CarSearch(brand='Toyota', model='Gt86', fuel='Essence')
    data = list(s())
    s.find_best(data, 20, {'gearbox': 'Manuelle', 'max_price': 23000, 'max_mileage': 50000})
    #res_gt86 = CarSearch('Toyota', 'Gt86', 'Essence')
    #count = 0
    #for x in res_gt86():
    #    count += 1
    #    #print(x['list_id'])
    #    print(x)
    #print(count)
    #res2_gt86 = CarSearch().prepare_input(res_gt86)
    #price = CarSearch().predict(res2_gt86, {'mileage': 40000, 'regdate': 2012, 'gearbox': 1, 'company_ad': 0})
    #pprint(res2)
    #print(price)

if __name__ == '__main__':
    main()
