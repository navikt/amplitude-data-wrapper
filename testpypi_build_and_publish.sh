source .env
rm -rf dist/
black .
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi ${!POETRY_TEST_TOKEN_PYPI}
poetry build
poetry publish -r testpypi #--build --dry-run