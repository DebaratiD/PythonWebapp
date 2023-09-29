# PythonWebapp
Python Microservices Webapp project

This application is a simple example of how microservices work and communicate with each other. The front-end is built using any popular framework, like angular, react, svelte or vue.
There are 2 services used in the backend. One is built using Django while the other is built using Flask. Both microservices are dockerised and use SQL for database storage. They communicate using RabbitMQ events and also have an internal API call from the main service to the admin service.

### Application setup
First installed django and django restframework using pip. Then created the django project using django-admin startproject command on cmd.
```bash
pip install django
pip install djangorestframework

django-admin startproject admin
```
Created a Dockerfile and docker-compose.yml file within the newly created django project. Also created requirements.txt to store all dependencies for the same.
