# VCF-data-manipulation project

## Requirements
- Python 3.8
- Django 4.0
- Django REST Framework
- REST Framework XML
- Django-rest-auth
- Django-extensions
- Pandas 1.3.5
- Coverage (Optional for testing)

## Installation
After you cloned the respository, you want to create a virtual environment, so you have a clean python installation. 
```
python -m venv env
```
Once you´ve created a virtual environment, you may activate it.
```
(On Windows): env\Scripts\activate.bat
(On Unix or MacOS): source env/bien/activate
```
You can install all the required dependencies by running
```
pip install -r requirements.txt
```

## Endpoints
In this REST API, you can find some endpoints that define its structure and how you can access data from the application using HTTP methods - GET, POST, PUT, DELETE.

Endpoint | HTTP Method | CRUD Method | Result
---|---|---|---
upload | POST | CREATE | Upload a vcf.gz file to django database
api | GET | READ | Get all VCF data
api/<str:ID> | GET | READ | Get a single row of VCF data
api | POST | CREATE | Create a new row of VCF data
api/<str:ID> | PUT | UPDATE | Update a row of VCF data
api/<str:ID> | DELETE | DELETE | Delete a row of VCF data
