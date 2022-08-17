source .env
rm -rf dist/
black .
poetry config pypi-token.pypi ${!POETRY_PYPI_TOKEN_PYPI}
poetry build
poetry publish