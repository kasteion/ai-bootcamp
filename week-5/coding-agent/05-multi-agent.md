# Multi-Agent Coding Assistant: Clarifier, Planner and Executor Agents

## Multi-Agent Architecture

We have our agent working. How about now we have a multi-agent setup?

The workflow consists of:

- Clarifier: Find out what the user wants to do
- Namer: Come up with a name for the project
- Planner: Prepare the technical requirements
- Executor: Implement the requirements

Execution flow:

1. clarifier
2. namer
3. planner
4. for each step from planner: executor
5. done
