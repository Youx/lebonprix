default: build

run:
	PYTHONPATH=. python3 lebonprix/middleware/api.py

uni:
	gunicorn lebonprix.middleware.api:app

build:
	python3 setup.py build

test:
	python3 setup.py test
