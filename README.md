# VCF-data-manipulation project

## Requirements
- Python 3.8
- Django 4.0
- Django REST Framework
- REST Framework XML
- Django-rest-auth
- Django-extensions
- Pandas 1.3.5
- CSV
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
register | POST | CREATE | Create new user
download | GET | READ | Download csv file of the database
api | GET | READ | Get all VCF data
api/<str:ID> | GET | READ | Get a single row of VCF data
api | POST | CREATE | Create a new row of VCF data
api/<str:ID> | PUT | UPDATE | Update a row of VCF data
api/<str:ID> | DELETE | DELETE | Delete a row of VCF data

## Use
You can test the API using cURL, httpie, Postman or a web browser (among other things). In this documentation I am going to show you how to test it with Postman and with the web browser for and easier understanding as these are the most visual options and the ones I used.

You can install Postman from [here](https://www.postman.com/downloads/).

First, you have to start up Django´s development server.
```
python manage.py runserver
```

### Upload VCF file
Now, open your web browser and we are going to upload a vcf.gz file to populate django´s database with the first 5 “CHROM,POS,ID,REF,ALT“ fields available on the VCF. In your browser type:
```
http://127.0.0.1:8000/upload/
```
You see now something like this:

![Upload site](/images/upload-site.png)

As you can see, you can select a file from your local machine and upload it clicking in the POST button.

If the file has the right format, a 201 CREATED is returned. If the file is in the wrong format, you will see the error message.

### Create User
We do not need to be authenticated to use the GET method and see all data or a single data (http://127.0.0.1:8000/api) but, we DO need to be authenticated to perform POST, PUT and DELETE.

So, to create a user you only need to do a POST request to http://127.0.0.1:8000/register/ with the username and password that you want to create.

![Create user](/images/create-user.png)

If the user is created succesfully, it will return your username and a 201 CREATED.


### GET
Get all VCF data: http://127.0.0.1/api/

- All VCF data will be displayed and paginated so you can nagivate to previous and next results.
- ACCEPT HTTP header options
	Accept header | Returns
	--- | ---
	application/json | Results as json
	application/xml | Results as xml
	None | Results as json
	\*/\* | Results as json
	Other | Code 406 (Not acceptable)
- The endpoint accepts a request parameter as part of the url (ID). So, if you want to receive the rows that match that specific ID, you go to: http://127.0.0.1/api/rs123, for example.
If there is a match, it returns the row/s that match. If there is no match, it returns 404 Not found.

### POST
Create new VCF row: http://127.0.0.1/api/

- The endpoint has to accept a HTTP AUTHORIZATION header to allow the request, so you need to pass Basic Authorization (username and password). You can do that in the browser by clicking in "Log In" at the top right corner.

![Log in](/images/log-in.png)

- It only accepts json data as input e.g.
	```
	{"CHROM": "chr1", "POS": 1000, "ALT": "A", "REF": "G", "ID": "rs123"}
	```
- If you are not logged in, you won´t have authorization and the POST request will return a 403 (Permission denied).
- If you are logged in, you have authorization and the POST request will return a 201 (Created).


### PUT
Update an existing VCF row: http://127.0.0.1/api/<str:ID>

- The endpoint has to accept a HTTP AUTHORIZATION header to allow the request, so you need to pass Basic Authorization (username and password). You can do that in the browser by clicking in "Log In" at the top right corner as shown in the POST request.

- You pass in the url the ID of the row that you want to modify.

- It only accepts json data as input. This contains the modification that you want to perform on the searched row. Then you click the button PUT.

- If the ID you are looking for does not exist, it returns a 404 (Not found).

- If you perform a succesfull update, it returns a 200 (Ok).

Example:

![PUT method](/images/put-delete.png)


### DELETE
It works exactly the same as the PUT request, the only difference is that you press the DELETE button because you want to make a delete request.

### Download database
You can download the database with all the changes into a csv file (with the five columns CHROM, POS, ID, REF, ALT).

You only need to go to (GET request): http://127.0.0.1/download/ and a csv would be downloaded to your local machine.

## TESTS
You can find tests for models and views here.


To run tests:
```
python manage.py test
```

To run tests with coverage:
```
coverage run --omit='*/venv/*' manage.py test
```



