
# justfile
default:
    just --list

run:
    uv run

install:
    uv sync --frozen

update:
    uv lock --upgrade

format:
    ruff check; \
    ruff format

# upgrade these from make and pip
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
