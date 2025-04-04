PYPI_PROJECT := "amplitude-data-wrapper"
IMPORT_PROJECT := "amplitude_data_wrapper"

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

test-install:
    uv run --with {{PYPI_PROJECT}} --no-project -- python -c "import {{IMPORT_PROJECT}}"

pypi_publish:
	$(PYTHON) -m twine upload --repository pypi dist/*

# $(PYTHON) -m twine upload --repository testpypi dist/*
testpypi_publish:
    uv publish --index testpypi