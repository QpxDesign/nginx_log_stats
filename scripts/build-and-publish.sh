rm dist/*
poetry build
python -m twine upload --repository pypi dist/* -u '__token__' -p $1
