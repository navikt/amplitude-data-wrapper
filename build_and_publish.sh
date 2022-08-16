source .env
rm -rf dist/
black .
poetry config pypi-token.pypi ${!project_token}
poetry build
poetry publish