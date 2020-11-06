# Sample django project with DRF and elasticsearch

## Main packages

- Django
- djangorestframework (DRF) (rest api)
- django-filter (add filter to DRF)
- django-rest-swagger (auto api document generator)
- drf-extensions (add some extensions to DRF)
- django-haystack (search with elasticsearch engine)
- drf-haystack (connect django-haystack to DRF)

## Prerequisites

- python 3.5 (may work with python 3.7 or 3.8)
- elasticsearch v2

## Usage

```
git clone <this repo>
cd rest-workspace
virtualenv -p python3.5 venv
source venv/bin/activate
pip install -r requirements.txt
./manage.py makemigrations
./manage.py migrate
./manage.py runserver
```

after run check this urls:

- [api with sqlite3 backend](127.0.0.1:8000/api/v1)
- [api with elasticsearch backend](127.0.0.1:8000/api/v1/search) (before use, run `./manage.py update_index`)
- [api documentation](127.0.0.1:8000/api-docs)

## Additional management commands

- update elasticsearch indexes
  
  `./manage.py update_index`

