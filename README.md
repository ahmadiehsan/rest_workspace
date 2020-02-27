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

- elasticsearch v2

### elasticsearch installation on ubuntu

add below lines to `elasticsearch2-installer.sh`

and run `bash elasticsearch2-installer.sh`

```
### Install Java
sudo apt-get update
sudo apt-get install openjdk-8-jdk openjdk-8-jre
java -version

### Download and install the Public Signing Key
wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -

echo "deb https://packages.elastic.co/elasticsearch/2.x/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list

### Install Elasticsearch
sudo apt-get update && sudo apt-get install elasticsearch -y

# Start elasticsearch
sudo service elasticsearch start

# Wait 10 seconds
sleep 10

### Make sure service is running
curl http://localhost:9200
```

## installation

```
git clone <this repo>
cd rest-workspace
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
  
  `./manage.py update_index --disable-change-limit`