# Django Project Setup Guide

## 1. Project Initialization & Repository Setup

- Create a project folder, e.g., `barcelona-football-store`, and initialize it as a Git repository. Using
- ```
    git init
  
- Inside the root directory, create a Python virtual environment and activate it: 
    ```bash
    python -m venv env
    env\Scripts\activate
    ```
- Create a `requirements.txt` listing essential dependencies like this
- ```bash
  django
  gunicorn
  whitenoise
  psycopg2-binary
  requests
  urllib3
  python-dotenv
put these inside `requirements.txt`

- Install dependencies:
  ```bash
  pip install -r requirements.txt

- After the dependencies are successfully downloaded, initilaize the Django project using this command
- ```bash
    django-admin startproject barcelona_football_store


- Inside `settings.py` ensure you add `localhost` and `127.0.0.1` to `ALLOWED_HOSTS` for local development:
- 
- now start the development server
- ```bash
    python manage.py runserver
- run this command inside the barcelona-football-store directory
- If its a success therefore its done and you can press `Ctrl + C` to exit the runserver and write `deactivate` on the terminal

- Now we can start creating the main application
- Run this
- ```bash
    python manage.py startapp main
- the main directory will be created and it will contain the structure for your Django app

- Register main applicatin on the project
- Open the `settings.py` file inside the `barcelona_football_store`
- add `main` to the bottom of the list of applications. You can find this in the INSTALLED_APPS

- Create a new directory named `templates` inside the `main`
- Create `main.html` inside templates
- And i've only filled it with <h1> Welcome to Barcelona Football Store </h1>

- Inside the `models.py` in the `main` directory, I filled it with this
- ```
    from django.db import models

  class Product(models.Model):
    name = models.CharField(max_length=255)  # item name
    price = models.IntegerField()  # item price
    description = models.TextField()  # item description
    thumbnail = models.URLField(max_length=500)  # item image URL
    category = models.CharField(max_length=100)  # item category
    is_featured = models.BooleanField(default=False)  # featured status

    def __str__(self):
        return self.name

- Since this is counted as a change into my database model we need to migrate this model by using this command
  ```bash
    python manage.py makemigrations

- To apply migration, run this
  ```bash
    python manage.py migrate


- Now, we connect views.py with the template we have earlier

- Open `views.py` inside `main`
- Fill it with this if you just want to display your html file
  ```bash
    from django.shortcuts import render
  def show_main(request):

    return render(request, "main.html")

- This code will render the html file by requesting `main.html` to the database and displaying it.

- Now we can start the routing
- create urls.py file in the main directory
- Write this code inside urls.py
  ```
    from django.urls import path
    from main.views import show_main

    app_name = 'main'

    urlpatterns = [
    path('', show_main, name='show_main'),
    ]

- now open urls.py inside barcelona_football_store and import include function
  ```
    from django.urls import path, include

- add the main.urls route into urlpatterns inside barcelona_football_store
  ```
    urlpatterns = [
      ...
      path('', include('main.urls')),
      ...
    ]

- Now we can push all of this into our repository
  run these command :
  ```
    git add .
    git commit -m "Complete tutorial 1: Django MVT implementation"
    git push origin master
    git push pws master



# Client Request Diagram
Client (Browser)
       |
       |  HTTP Request (e.g., /store/)
       v
-------------------
|     urls.py     |
-------------------
       |
       |  Matches URL pattern
       v
-------------------
|     views.py    |
-------------------
       |
       |  (Optional) Query database
       v
-------------------
|    models.py    |
-------------------
       |
       |  Data returned
       v
-------------------
|   HTML Template |
-------------------
       |
       |  Rendered HTML
       v
Client (Browser)
       ^
       |  HTTP Response (HTML page)


# Role of settings.py
The settings.py file in a Django project acts as the central configuration hub that controls how the application behaves. 
It defines critical settings such as lists active applications in INSTALLED_APPS; and specifies middleware for handling requests and responses. 
It also manages database connections, template directories, and static and media file paths In short, settings.py is the brain of a Django project, ensuring all components work together consistently and securely.

# How Database Migration Works
In Django, database migration is the process of keeping your database schema (tables, fields, relationships) in sync with the models you define in models.py. When you create or modify models, Django doesn’t automatically change the database; instead, you generate a migration file that describes the changes.
This works in two main steps: first, run python manage.py makemigrations to create migration files that record the changes in your models (like adding a field or creating a table), then run python manage.py migrate to apply those migrations and update the actual database schema. 
This system ensures that your database structure evolves safely alongside your code, while also keeping a history of changes that can be rolled back or reapplied when needed.

# Why Django is easy
I believe Django is easy to understand because it is pretty straight forward unlike any javascript framework out there
and the way to connect the urls and the templates are the easiest out there.





