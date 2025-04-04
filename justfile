# load env variables
set dotenv-load

# env variables
TESTPYPI_TOKEN := env('TESTPYPI_TOKEN')
PYPI_TOKEN := env('PYPI_TOKEN')
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

build:
	rm -rf dist/; \
	uv build

# test package can be installed and imported
test-install:
    uv run --with {{PYPI_PROJECT}} --no-project -- python -c "import {{IMPORT_PROJECT}}"

# publish on python package index
pypi_publish:
    uv publish --token {{PYPI_TOKEN}}

# publish on test python package index
testpypi_publish:
    uv publish --index testpypi --token {{TESTPYPI_TOKEN}}
