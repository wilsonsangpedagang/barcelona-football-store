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

# Assignment 4

## Authentication Form Pros and Cons
AuthenticationForm from Django is Django’s built-in login form. It accepts credentials (by default username + password), uses django.`contrib.auth.authenticate()` to validate them, and exposes helpful helpers such as `get_user()` and `confirm_login_allowed()`.

### Advantages

- Ready to use: saves boilerplate (form validation + call to `authenticate()`).

- Integrates with Django auth backends out of the box.

- Handles inactive users via `confirm_login_allowed`.

- Proper error messages and form API for templates.

- Works well with `django.contrib.auth.login()`.

### Disadvantages

- Minimal: only username/password by default (not email-first login).

- Not opinionated about extra security (no built-in rate limiting, lockout, or 2FA).

- UI/fields require subclassing to customize (e.g., add `remember_me`, email login).

- Doesn’t implement account throttling — needs extra packages (e.g., django-axes) for that.

## Authentication vs Authorization — difference & how Django implements them
#### Authentication (AuthN)

- Definition: Who are you? — verifying identity (username/password, tokens, OAuth, etc.).

Django implementation:

- `django.contrib.auth` with User model and pluggable authentication backends.

- `authenticate()` checks credentials using backends.

- `login(request, user)` sets session and marks user as authenticated `(request.user)`.

`-AuthenticationForm` helps validate credentials.

#### Authorization (AuthZ)

Definition: What are you allowed to do? — permissions, roles, access control.

Django implementation:

- Model-level permissions via `user.has_perm('app.change_model')` and `Model._meta.permissions`.

- `Group` objects to bundle permissions.

- Decorators: `@login_required`, `@permission_required('app.change_model')`, `UserPassesTestMixin`, `PermissionRequiredMixin`.

- For object-level permissions you need third-party libs (e.g., django-guardian) or custom checks in views.

## Sessions vs Cookies for storing state (benefits & drawbacks)

### Benefits

Simple to implement.

Persistent across browser sessions (if not session cookie).

Good for small user preferences or client-only state.

### Drawbacks

Visible to client — don’t store sensitive info (even if signed).

Vulnerable to theft via XSS unless HttpOnly is set.

Size-limited.

Forgery risk if not signed/validated.

### Sessions (server-side, cookie holds only session id)

Django default: server stores session data (database, cache, or signed cookie backend). Browser receives only a session cookie like sessionid.

### Benefits

Sensitive data kept server-side.

More storage capacity (not limited by cookie size).

Server controls lifecycle (invalidate sessions centrally).

### Drawbacks

Requires server storage (DB/Cache); scaling needs shared session store across web servers (Redis, Memcached).

Still depends on session cookie — session id theft can impersonate user.

Extra complexity for distributed deployments (sticky sessions or shared store).

## Are cookies secure by default? Risks & how Django helps

Are cookies secure by default?
No cookies have default properties that vary by environment, and by default they are not automatically safe for production (e.g., Secure flag is often off in dev). Cookies are susceptible to:

- XSS (JavaScript reads cookies unless HttpOnly),

- CSRF (for state-changing requests),

- Network eavesdropping unless Secure + HTTPS,

- Session fixation / theft if session id is reused.

How Django mitigates these

- CSRF protection: CsrfViewMiddleware + {% csrf_token %}. Tokens prevent forged POSTs.

## Step by Step Tutorial
Start by updating your Product model to use settings.AUTH_USER_MODEL for a user ForeignKey and set null=True, blank=True so existing rows won’t break; run python manage.py makemigrations and python manage.py migrate to create the column, and if you need to populate existing products create a simple data migration or run a script to assign a default user, then (optionally) change the field to null=False and re-run migrations. Next implement the auth views (login/register/logout) using AuthenticationForm and UserCreationForm, call login(request, user) (which rotates the session) and logout(request) and handle “remember me” with request.session.set_expiry(...). Put all path() entries inside a single urlpatterns = [...] list and name them (login, register, logout, main) so your templates can use {% url 'register' %}; make sure templates include {% csrf_token %}. Protect pages with @login_required and use permission_required or explicit object-level checks (request.user == product.user) for authorization. Harden production security by setting SESSION_COOKIE_SECURE = True, SESSION_COOKIE_HTTPONLY = True, SESSION_COOKIE_SAMESITE = 'Lax', enabling CSRF middleware, and using HTTPS/HSTS/CSP as appropriate. Run your tests and verify flows locally, then commit changes (git add . → git commit -m "..."), fetch remote changes (git fetch origin) and either git rebase origin/master (resolve conflicts, git rebase --continue) or git pull --no-rebase origin master to merge, and finally git push origin master (use --force-with-lease only as a last resort). In production, always run migrations on the server/container before restarting Gunicorn so the DB schema and code stay in sync.

# Assigment 5

### CSS Selector Priority

When multiple CSS selectors apply to the same HTML element, browsers decide which style to apply based on specificity. The order of priority is:

Inline styles – Styles directly added to the element using the style attribute have the highest priority.
```html
<p style="color: red;">Hello</p>
```

ID selectors – Selectors that use an element's ID (#id) are more specific than class or element selectors.

```html
#myParagraph { color: blue; }
```

Class, attribute, and pseudo-class selectors – These include .class, [attribute=value], :hover, :nth-child().

```html
.highlight { color: green; }
```

Element and pseudo-element selectors – Selectors that target the tag name directly (p, div) or pseudo-elements (::before, ::after) have the lowest specificity.

```css
p { color: black; }
```

### Responsive Design
Responsive design ensures that a web application looks good and functions well across different devices (desktop, tablet, mobile) and screen sizes.

- Importance in Web Application Development:

- Improves user experience on all devices.

- Enhances accessibility and usability.

- Boosts SEO (search engines prefer mobile-friendly websites).

- Reduces the need to maintain multiple versions of a site.

Examples:

- Implemented:

Google.com – Adjusts layout based on screen size. Search bar and buttons scale for mobile.

- Not implemented:

Some older corporate websites still force desktop layouts on mobile, causing horizontal scrolling and unreadable text.

Reasons:

- Implemented examples use CSS media queries, flexible images, and adaptive layouts.

- Non-implemented examples often lack media queries, fixed-width layouts, or use tables for layout, which is not mobile-friendly.

### Box Model
Every HTML element can be thought of as a box with four layers:

1. Content – The actual content like text or image.

2. Padding – Space between the content and the border.

```css
padding: 10px;
```

3. Border – A line surrounding the padding and content.

```css
border: 2px solid black;
```

4. Margin – Space outside the border, separating this element from others.

```css
margin: 15px;
```

Implementation:
```css
div {
    margin: 20px;
    border: 2px solid red;
    padding: 10px;
}
```

### Layout Systems
A. Flexbox
- Purpose: One-dimensional layout system (row OR column).

- Use case: Align items horizontally or vertically, distribute space evenly.

Example:

```css
.container {
    display: flex;
    justify-content: space-between; /* Horizontal spacing */
    align-items: center;           /* Vertical alignment */
}
```

B. Grid
- Purpose: Two-dimensional layout system (row AND column).

- Use case: Complex layouts like dashboards or magazine-style pages.

Example:
```css
.container {
    display: grid;
    grid-template-columns: 1fr 2fr 1fr;
    gap: 10px;
}
```

Difference:
- Flexbox is simpler for linear alignment (row/column).

- Grid is better for complex, multi-directional layouts.


### Implementation

I made 2 new functions in views.py, edit_product and delete_product.

I customize all of my pages using tailwind, changing all of the color into Barcelona theme with these color palette.

```bash
#a50044 # dark red
#004d98 # dark blue
#edbb00 # orange
#ffed02 # yellow
#db0030 # light red
```

I also made the product_card for the newest product published by the website.

I made the navbar using the same color scheme that contains Home and Create Product (for now)


# Assignment 6

# Understanding Synchronous vs Asynchronous Requests and AJAX in Django

## Synchronous vs Asynchronous Requests

### Synchronous Request
- Blocks the client until receiving a response from the server
- User must wait for the page to reload completely
- Sequential processing: one request at a time
- Example: Traditional form submission that refreshes the entire page

### Asynchronous Request
- Non-blocking: allows other operations to continue while waiting for response
- No page reload required
- Multiple requests can be handled simultaneously
- Example: Updating a chat message without refreshing the page

## AJAX in Django: Request-Response Flow

1. **Client-side Initiation**
   - JavaScript creates an XMLHttpRequest or uses Fetch API
   - Data is prepared (if needed) for sending to server

2. **Request Processing**
   ```javascript
   fetch('/api/endpoint/', {
       method: 'POST',
       body: JSON.stringify(data),
       headers: {
           'X-CSRFToken': csrfToken,
           'Content-Type': 'application/json'
       }
   })
   ```

3. **Django Server-side**
   - View receives the AJAX request
   - Processes the data
   - Returns JSON response instead of HTML

4. **Client-side Completion**
   - JavaScript receives the response
   - Updates DOM accordingly without page reload

## Advantages of AJAX in Django

1. **Better User Experience**
   - No full page reloads
   - Smoother interactions
   - Faster response times

2. **Reduced Server Load**
   - Only necessary data is transferred
   - Lower bandwidth usage
   - Partial page updates instead of full renders

3. **Enhanced Interactivity**
   - Real-time updates possible
   - Dynamic content loading
   - Better form handling

## Security Measures for AJAX Login/Register

1. **CSRF Protection**
   ```javascript
   // Include CSRF token in AJAX headers
   const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
   ```

2. **Input Validation**
   - Client-side validation
   - Server-side validation
   - Sanitize all input data

3. **HTTPS Usage**
   - Encrypt all data transmission
   - Prevent man-in-the-middle attacks

4. **Rate Limiting**
   - Implement request limits
   - Prevent brute force attacks

5. **Session Management**
   - Secure session handling
   - Proper authentication checks

## AJAX Impact on User Experience (UX)

1. **Positive Impacts**
   - Faster perceived load times
   - No page refresh interruptions
   - Smoother interactions
   - Better feedback mechanisms
   - Enhanced responsiveness

2. **Considerations**
   - Need for loading indicators
   - Proper error handling
   - Browser history management
   - Accessibility considerations
   - Fallback mechanisms for when JavaScript is disabled

3. **Best Practices**
   - Show loading states
   - Provide clear feedback
   - Handle errors gracefully
   - Maintain browser navigation
   - Ensure progressive enhancement








