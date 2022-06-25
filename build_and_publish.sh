rm -rf dist/
black .
poetry build
poetry publish