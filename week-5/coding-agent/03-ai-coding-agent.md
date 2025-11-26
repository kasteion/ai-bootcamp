# AI Coding Agent

Now that we have the tools, let's create the agent that will use them to modify Django projects based on user instructions.

## Simple Prompt

We start with something simple:

```python
coding_instructions = """
You are a coding agent. Your task is to modify the provided
Django project template according to user instructions.
"""
```

This basic prompt tells the agent its role, but doesn't provide much context.

## Comprehensive Prompt

Eventually we can get to something like that:

```python
coding_instructions = """
You are a coding agent. Your task is to modify the provided Django project template
according to user instructions. You don't tell the user what to do; you do it yourself using the
available tools. First, think about the sequence of steps you will do, and then
execute the sequence.
Always ensure changes are consistent with Django best practices and the project's structure.

## Project Overview

The project is a Django 5.2.4 web application scaffolded with standard best practices. It uses:
- Python 3.8+
- Django 5.2.4 (as specified in pyproject.toml)
- uv for Python environment and dependency management
- SQLite as the default database (see settings.py)
- Standard Django apps and a custom app called myapp
- HTML templates for rendering views
- TailwindCSS for styling

## File Tree

├── .python-version
├── README.md
├── manage.py
├── pyproject.toml
├── uv.lock
├── myapp/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── templates/
│   │   └── home.html
│   ├── tests.py
│   └── views.py
├── myproject/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── templates/
    └── base.html

## Content Description

- manage.py: Standard Django management script for running commands.
- README.md: Setup and run instructions, including use of uv for dependency management.
- pyproject.toml: Project metadata and dependencies (Django 5.2.4).
- myapp/: Custom Django app with models, views, admin, tests, and a template (home.html).
  - migrations/: Contains migration files for database schema.
- myproject/: Django project configuration (settings, URLs, WSGI/ASGI entrypoints).
  - settings.py: Configures installed apps, middleware, database (SQLite), templates, etc.
- templates/: Project-level templates, including base.html.

You have full access to modify, add, or remove files and code within this structure using your available tools.


## Additional instructions

- Don't execute "runproject", but you can execute other commands to check if the project is working.
- Make sure you use TailwindCSS styles for making the result look beatiful
- Keep the original URL for TailwindCSS
- Use pictograms and emojis when possible. Font-awesome is awailable
- Avoid putting complex logic to templates - do it on the server side when possible
"""
```

This comprehensive prompt provides the agent with project structure, technology stack, and specific guidelines for making changes.

## Running the Agent

Let's use it:

```python
from openai import OpenAI

from toyaikit.tools import Tools
from toyaikit.chat import IPythonChatInterface
from toyaikit.llm import OpenAIClient
from toyaikit.chat.runners import OpenAIResponsesRunner

tools_obj = Tools()
tools_obj.add_tools(agent_tools)

chat_interface = IPythonChatInterface()
llm_client = OpenAIClient()

runner = OpenAIResponsesRunner(
    tools=tools_obj,
    developer_prompt=coding_instructions,
    chat_interface=chat_interface,
    llm_client=llm_client
)

runner.run()
```

This sets up the agent with the tools we created earlier, connects it to the OpenAI API, and starts an interactive chat session.

## Using the Agent

Now tell it about the app you want to implement!

Describe the features you want, and the agent will use the available tools to read, write, and modify files in your Django project.

## Testing Your Project

After that, go to the project directory and run it:

```bash
make run
```

Open your browser to localhost:8000 to see the result.

If it doesn't work - continue your conversation with the agent until it's fixed. The agent can debug and iterate on the code based on your feedback.
