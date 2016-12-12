#!/usr/bin/env python3

from lebonprix.crawler.car_search import CarSearch
import json

def main():
    res_207 = CarSearch('Peugeot', '207', 'Essence', 'vti')
    data = []
    for x in res_207():
        data.append(x)
    with open("data.json", 'w') as fd:
        fd.write(json.dumps(data))

    price = res_207.predict(data, {'gearbox': 'Manuelle', 'regdate': 2007, 'company_ad': 0, 'mileage': 110000})
    print(price)
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
