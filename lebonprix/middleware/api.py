from lebonprix.crawler.car_search import CarParamModel, CarParamFuel, CarSearch
import flask

app = flask.Flask(__name__)


@app.route("/api/cars/params/brand_model")
def list_brands_and_models():
    return flask.json.jsonify(CarParamModel.MODELS)

@app.route("/api/cars/params/fuel")
def list_fuels():
    return flask.json.jsonify(sorted(CarParamFuel.VALUES, key=CarParamFuel.VALUES.get))

@app.route("/api/cars/params/gearbox")
def list_gearbox():
    return flask.json.jsonify(['Manuelle', 'Automatique'])


@app.route("/api/cars/predict", methods=['POST'])
def predict_price():
    data = flask.request.get_json()
    search = CarSearch(brand=data['brand'], model=data['model'], fuel=data['fuel'], detail=data['spec'])
    search_results = list(search())
    samples = [
        {'title': result['subject'],
         'picture': result['thumb']}
        for result in search_results[:10]
    ]
    price = search.predict(search_results, {'gearbox': data['gearbox'], 'regdate': data['regdate'],
                                            'company_ad': data['company_ad'], 'mileage': data['mileage']})
    return flask.json.jsonify({'price': int(price[0]), 'sample_size': len(search_results), 'samples': samples})


if __name__ == '__main__':
    app.run()
