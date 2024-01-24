rm dist/*
poetry build
python3 -m twine upload --repository pypi dist/* -u '__token__' -p $1