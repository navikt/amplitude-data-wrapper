PYTHON=python3.10
VENV= .venv/bin/activate

install:
	source $(VENV); \
	pip install --upgrade pip-tools pip setuptools; \
	$(PYTHON) -m piptools compile -o requirements/main.txt pyproject.toml; \
	$(PYTHON) -m piptools compile --extra dev -o requirements/dev.txt pyproject.toml; \
	pip install -r requirements/main.txt -r requirements/dev.txt

update-deps:
	source $(VENV); \
	pip install --upgrade pip-tools pip setuptools; \
	$(PYTHON) -m piptools compile --upgrade --resolver backtracking -o requirements/main.txt pyproject.toml; \
	$(PYTHON) -m piptools compile --extra dev --upgrade --resolver backtracking -o requirements/dev.txt pyproject.toml

init:
	source $(VENV); \
	pip install --editable .; \
	pip install --upgrade -r requirements/main.txt  -r requirements/dev.txt

update: update-deps init

build:
	source $(VENV); \
	rm -rf dist/; \
	$(PYTHON) -m build

pypi_publish:
	source $(VENV); \
	$(PYTHON) -m twine upload --repository pypi dist/*

testpypi_publish:
	source $(VENV); \
	$(PYTHON) -m twine upload --repository testpypi dist/*

mypy:
	source $(VENV); \
	mypy src

format:
	source $(VENV); \
	isort src; \
	black --exclude .venv/ .