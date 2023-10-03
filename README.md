# PythonWebapp
### Python Microservices Webapp project
This project is created by referring this [youtube tutorial](https://www.youtube.com/watch?v=0iB5IPoTDts).

This application is a simple example of how microservices work and communicate with each other. The front-end is built using any popular framework, like angular, react, svelte or vue.
There are 2 services used in the backend. One is built using Django while the other is built using Flask. Both microservices are dockerised and use SQL for database storage. They communicate using RabbitMQ events and also have an internal API call from the main service to the admin service.



## Application setup
### Creating the Django app

First installed **django** and **django restframework** using pip. Then created the django project using django-admin startproject command on cmd.
```
pip install django
pip install djangorestframework

django-admin startproject admin
```
Created a `Dockerfile` and `docker-compose.yml` file within the newly created django project. Also created requirements.txt to store all dependencies for the same.
Once Dockerfile is created, use `docker-compose up` command to build the backend. Make sure that Docker desktop is connected to avoid connection error. 



### Connecting to MySQL server

For the database, make sure to use the database client extension on vscode. Here, specify the name, port and db language for the database and connect.
To create the products app, in the terminal, use 
```bash
docker-compose exec backend sh
```
to start a java command section. Input another command, `python manage.py startapp products` to automatically create the folder structure for the new products app. Once the products app is created, open models.py to create the schemas that the products app will be using. In settings.py under admin, add the details of the database, like the login credetials(username, password, host, port), cors_origin_allow_all setting, middleware modifications and installed_apps additions.

The models and must now be migrated to create tables for the database. To do so, while still being connected to Docker, run 

```bash
docker-compose exec backend sh

python manage.py migrations

python manage.py migrate
```

To clarify, this is a Django project that has been built using 
```bash
django-admin startproject admin
``` 
command and connected to MySQL database by making changes in the settings.py file. For the database, the port used is 3306 by the docker container which is the default container for MySQL server. External port will be 33066. When running `docker-compose up`, Docker will first initialize the db since the main app depends on it. The  `restart: always` spec makes sure that the failure prone MySQL server will restart everytime in such an event. The `volumes` spec mentions where the db data is to be stored in the app directory.

### Serializers
To return objects in the API, we need to use serializers. We will be using serializers only for the Products model as random IDs will be returned for Users model.

### Setting up API endpoints
For the Products app, we will set up the API endpoints in views.py file where we create 5 functions. The list and create functions are for generally getting the list of all products and creating a new product. The retrieve, update and destroy functions are get, put and delete operations respectively on a product item.

Once the endpoints are setup, the corresponding urls are specified in the urls.py file. Here, for each route, the operation and respective function are added.

The urls added in the products app must be accessible from the admin project. To do so, in the urls.py file of admin, use `include` to create a new url called `api` and add the routes from products app.
```bash
path('api/', include('products.urls'))
```
Use Postman to check if your api endpoints are working right.

In the views.py file, another class **User** is created that behaves as an API to the User table. The get function simply returns a random user from the table using the `random` function.

### Flask application

Create a folder main and within that a main.py file.
Add the modules or packages needed to be installed in requirement.txt. There might be lot of issues coming up from the `__init__.py` file of flask. The current requirements.txt file in this project does not currently give any error. 

To migrate models from flask app to mysql, you need to be able to use the flask db commands.

To connect to MySQL server, run the following commands (after creating a manager.py file that will enable db migration and specifying the models needed in main.py):

In terminal 1:
```
cd main
docker-compose up
```

In terminal 2:
```
docker-compose exec backend sh
python manager.py db --help
python manager.py db init
python manager.py db migrate
python manager.py db upgrade
```

Before the last upgrade command in terminal 2, create and connect to a mysql db connection using database client at port 33067 named main.


### RabbitMQ setup