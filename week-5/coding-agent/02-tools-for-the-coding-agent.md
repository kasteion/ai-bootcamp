# Tools for the Coding Agent

## Starting a New Project

First, we need a function to copy the template into a separate folder:

```python
import os
import shutil


def start(project_name):
    if not project_name:
        print("Project name cannot be empty.")
        return False

    if os.path.exists(project_name):
        print(f"Directory '{project_name}' already exists. Please choose a different name or remove the existing directory.")
        return False

    shutil.copytree('django_template', project_name)
    print(f"Django template copied to '{project_name}' directory.")

    return True
```

This function validates the project name and copies the template directory. This is how we use it:

```python
project_name = input("Enter the new Django project name: ").strip()
start(project_name)
```

## Creating Agent Tools

Next, we need to define a few functions for the agent:

- List files
- Read file
- Write file
- Execute a bash command
- Do grep

We will use ChatGPT (or AI Coding Assistant) for creating these files.

You can see the result in [tools.py](https://github.com/alexeygrigorev/ai-bootcamp-codespace/blob/main/week5/1-coding-agent/tools.py). Alternatively, you can see the file that we created with ChatGPT during the lesson here ([tools2.py](https://github.com/alexeygrigorev/ai-bootcamp-codespace/blob/main/week5/1-coding-agent/tools2.py)).

Note: for bash, you want to disable running "runserver" - if you allow the agent to run it in Jupyter, it will hang up the environment.

## Using the AgentTools Class

So if we put the code inside a class AgentTools, we can use it like that:

```python
import tools
from pathlib import Path

project_path = Path(project_name)
agent_tools = tools.AgentTools(project_path)
```

Let's test it.

## Modifications for UV Environment

A few things we may need to modify:

To run things inside uv, ensure all commands are prefixed with uv run:

```python
commands = command.split('&&')

new_commands = []

for c in commands:
    c = c.strip()

    if 'uv run' not in c:
        c = 'uv run ' + c

    new_commands.append(c)

final_command = (' && '.join(new_commands)).strip()
print(f"executing '{final_command}'...")
```

This ensures commands run in the correct UV virtual environment.

If it complains about VIRTUAL_ENV, remove it from the environment:

```python
import os
del os.environ['VIRTUAL_ENV']
```

This prevents conflicts between Jupyter's environment and the project's UV environment.
