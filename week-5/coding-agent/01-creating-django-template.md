# Creating a Django Template Project

## Option 1: Using the Pre-built Template

You can download the template that is already working

Clone the repository with a working Django template:

```bash
git clone https://github.com/alexeygrigorev/django_template.git
```

Install dependencies, activate the database and run it:

```bash
cd django_template
uv sync

make migrate
make run
```

Open localhost:8000 in your browser to see the running application.

## Option 2: Build from Scratch

Follow these steps to create a Django project from the ground up.

### Initialize the Project

Let's start a new Django project with uv as the package manager:

```bash
mkdir django_template
cd django_template/

uv init
rm main.py

uv add django

uv run django-admin startproject myproject .
uv run python manage.py startapp myapp
```

This creates a Django project named myproject and an app named myapp.

### Register the App

Add the new app (myapp) into `myproject/settings.py`'s INSTALLED_APPS:

```python
# filepath: myproject/settings.py
INSTALLED_APPS = [
    # ...existing code...
    'myapp',
]
```

### Create a Makefile

For our convenience, we can have a Makefile with useful commands for common tasks:

```Makefile
# filepath: Makefile
.PHONY: install migrate run

install:
	uv sync --dev

migrate:
	uv run python manage.py migrate

run:
	uv run python manage.py runserver
```

This allows you to run make migrate and make run instead of typing the full commands.

### Set Up Templates

Next, create the base HTML template in `templates/base.html`:

```html
<!-- filepath: templates/base.html -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}{% endblock %}</title>
  </head>
  <body>
    {% block content %}{% endblock %}
  </body>
</html>
```

Add this templates directory to the settings file so Django can find it:

```python
# filepath: myproject/settings.py
TEMPLATES = [{
    'DIRS': [BASE_DIR / 'templates'],
    # ...existing code...
}
```

### Create Views and URLs

Now we're ready to create the home view for our app:

```python
# filepath: myapp/views.py
# ...existing code...
def home(request):
    return render(request, 'home.html')
```

```python
# filepath: myproject/urls.py
# ...existing code...
from myapp import views

urlpatterns = [
    # ...existing code...
    path('', views.home, name='home'),
]
```

### Create the Home Template

HTML code for `myapp/templates/home.html`:

```html
<!-- filepath: myapp/templates/home.html -->
{% extends 'base.html' %} {% block content %}
<h1>Home</h1>
{% endblock %}
```

This template extends the base template and adds a simple heading.

### Add Styling Libraries

Finally, let's add TailwindCSS and Font-Awesome to our base.html template for styling:

```html
<!-- filepath: templates/base.html -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- ...existing code... -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css"
      rel="stylesheet"
    />
  </head>
  <!-- ...existing code... -->
</html>
```

We can update `base.html` with this code for a more complete layout.

Create the styles in `static/css/styles.css`:

```css
/* Main h1 styling */
main h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  text-align: center;
  margin-bottom: 2rem;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-bottom: 3px solid #e5e7eb;
  border-radius: 8px;
  transition: all 0.3s ease;
}

/* Additional custom styles */
.custom-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.custom-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

/* Custom card styling */
.custom-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  main h1 {
    font-size: 2rem;
    padding: 0.75rem;
  }
}
```

And add the path to the `static/css` folder, so Django knows how to load it:

```python
# filepath: myproject/settings.py
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

Now the template is ready!

## Summary

You now have a working Django project with:

- A configured app (myapp)
- Template inheritance with a base layout
- TailwindCSS for styling
- Font-Awesome for icons
- A Makefile for convenient commands
