# sample django rest framework project

## main packages

- Django
- djangorestframework (DRF) (rest api)
- django-filter (add filter to DRF)
- django-rest-swagger (auto api document generator)
- drf-extensions (add some extensions to DRF)
- django-haystack (search with elasticsearch engine)
- drf-haystack (connect django-haystack to DRF)

## prerequisites

- python 3.5
- elasticsearch v2

[python 3.5 installation](https://mgit.mparsict.com/ahmadiehsan/cheatsheet/tree/master/python)

[elasticsearch 2 installation](https://mgit.mparsict.com/ahmadiehsan/cheatsheet/tree/master/elasticsearch)

## project installation

```
git clone <this repo>
cd rest-workspace
virtualenv -p python3.5 venv
source venv/bin/activate
pip install -r req.txt
./manage.py makemigrations
./manage.py migrate
./manage.pu runserver
```

after install check this urls:

- 127.0.0.1:8000/api/v1 (api with sqlite3 backend)
- 127.0.0.1:8000/api/v1/search (api with elasticsearch backend)
- 127.0.0.1:8000/api-docs (api documentation)

## additional management commands

- update elasticsearch indexes
  
  `./manage.py update_index`
