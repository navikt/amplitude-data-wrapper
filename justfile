# load env variables
set dotenv-load

# env variables
TESTPYPI_TOKEN := env('TESTPYPI_TOKEN')
PYPI_TOKEN := env('PYPI_TOKEN')
PYPI_PROJECT := "amplitude-data-wrapper"
IMPORT_PROJECT := "amplitude_data_wrapper"

# list recipes
default:
    just --list

# install and run
run:
    uv run

# install dependencies
install:
    uv sync --frozen

# upgrade dependencies
update:
    uv lock --upgrade

# check code with ruff
check:
    ruff check

# format with ruff
format:
    ruff format

# build package
build: check format
	rm -rf dist/; \
	uv build

# test package can be installed and imported
package-test:
    uv run --with {{PYPI_PROJECT}} --no-project -- python -c "import {{IMPORT_PROJECT}}"

# publish on python package index
pypi_publish:
    uv publish --token {{PYPI_TOKEN}}

# publish on test python package index
testpypi_publish:
    uv publish --index testpypi --token {{TESTPYPI_TOKEN}}
