default: build

run:
	PYTHONPATH=. python3 lebonprix/middleware/api.py

build:
	python3 setup.py build

test:
	python3 setup.py test
