
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
	rm -rf dist/; \
	uv build

pypi_publish:
	$(PYTHON) -m twine upload --repository pypi dist/*

testpypi_publish:
	$(PYTHON) -m twine upload --repository testpypi dist/*
