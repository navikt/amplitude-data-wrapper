install:
	pip install --upgrade pip-tools pip setuptools
	pip-compile --output-file requirements/main.txt requirements/main.in
	pip-compile --output-file requirements/dev.txt requirements/dev.in
	pip install -r requirements/main.txt -r requirements/dev.txt

update-deps:
	pip install --upgrade pip-tools pip setuptools
	pip-compile --upgrade --build-isolation --output-file requirements/main.txt requirements/main.in
	pip-compile --upgrade --build-isolation --output-file requirements/dev.txt requirements/dev.in

init:
	pip install --editable .
	pip install --upgrade -r requirements/main.txt  -r requirements/dev.txt

update: update-deps init

build:
	rm -rf dist/
	python -m build

pypi_publish:
	python -m twine upload --repository pypi dist/*

testpypi_publish:
	python -m twine upload --repository testpypi dist/*
