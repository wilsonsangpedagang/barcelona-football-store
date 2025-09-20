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

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

1. Why do we need data delivery in implementing a platform?
Because a platform (like a web app, mobile app, or API) doesn’t live in isolation.
It usually needs to communicate data:
From backend → frontend (e.g., sending products from a database to be shown on a webpage).
From frontend → backend (e.g., submitting a form).
Between different systems/services (e.g., your platform calling an external payment API).
Without data delivery, a platform would just be static — no dynamic content, no interaction, and no integration with other services.

2. Which is better, XML or JSON? Why is JSON more popular than XML?
Both XML and JSON are data interchange formats with different strengths. XML supports metadata with attributes and namespaces and is very strict, making it suitable for complex hierarchical data, but it is also very verbose and slower to parse. JSON, on the other hand, is lightweight, less verbose, easier to read and write, and maps directly to data structures in most programming languages such as objects, lists, and key-value pairs. It is also faster to parse and widely supported by JavaScript and modern APIs, although it offers less support for metadata compared to XML. JSON has become more popular because it is lighter, faster, easier to use, and works natively in JavaScript without additional parsing, while XML is still commonly used in enterprise and legacy systems such as SOAP and document standards.

3. What is the purpose of the is_valid() method in Django forms, and why do we need it?
The is_valid() method in Django forms is used to validate the data submitted by the user against the form’s defined fields and constraints. It checks whether the data is complete, correctly formatted, and adheres to the rules set in the form. This validation process is important to prevent errors and ensure that only clean and reliable data is processed or saved to the database.

4. Why do we need a csrf_token when making forms in Django? What can happen if we don't include a csrf_token in a Django form? How can this be exploited by an attacker?
A csrf_token is required in Django forms to protect against Cross-Site Request Forgery (CSRF) attacks. If it is not included, an attacker could exploit the vulnerability by tricking a logged-in user into unknowingly submitting malicious requests, such as changing sensitive account details or performing unauthorized actions. By using a csrf_token, Django ensures that form submissions are authentic and originate from trusted sources within the application.

First, I created four new view functions inside the views.py file. These functions were responsible for returning the model objects in both XML and JSON formats, as well as filtering them by ID. To achieve this, I used Django’s serializers module to serialize the querysets into the desired format. For example, I made one function that serialized all objects into XML, another for JSON, and then two more functions that accepted an ID parameter to return a single object in XML or JSON.

Next, I moved to the urls.py file of the app to register the URL routings. For each of the four view functions, I defined a corresponding URL pattern. This ensured that when the URL was accessed, it would trigger the correct view and return the data in the requested format.

After setting up the views and routes, I worked on the main webpage for displaying the model object data. In the template file product.html, I used a loop to display all available objects and added an "Add" button that redirected to the form page using Django’s {% url %} template tag. For each listed object, I also included a "Detail" button, which linked to the detail page of that specific object.

Following that, I created a form page in product_form.html. This page used Django’s form handling system, where the form submission would be processed in the views.py file. Upon submission, the new object would be saved into the database, and the user would be redirected back to the product list page to see the updated list.

Finally, I built a detail page in product_detail.html. This template displayed all the information about a single model object, which was passed from a dedicated view function in views.py. The view fetched the object based on its ID and sent it to the template for rendering.

<img width="1366" height="768" alt="Screenshot 2025-09-16 124410" src="https://github.com/user-attachments/assets/511147d3-cb86-4063-b7e2-9c815fdc16a3" />
<img width="1366" height="768" alt="Screenshot 2025-09-16 124433" src="https://github.com/user-attachments/assets/c74f8c8f-71aa-4c0d-a872-b9246172c6dd" />






