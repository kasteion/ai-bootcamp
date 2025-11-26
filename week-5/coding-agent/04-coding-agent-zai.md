# Coding Agent with Z.ai

## Setting Up the Z.ai Client

Z.ai, like most LLM providers, follows OpenAI API, so we can just use the OpenAI client:

```python
from openai import OpenAI

zai_client = OpenAI(
    api_key=os.getenv('ZAI_API_KEY'),
    base_url='https://api.z.ai/api/paas/v4/'
)
```

This creates a client that points to Z.ai's API endpoint using your Z.ai API key.

## API Compatibility

It doesn't support the responses API like OpenAI's latest models, so we will need to use the older chat.completions API.

This means we'll use different runner and client classes from toyaikit.

## Creating the Agent with Z.ai

The rest is similar, including tools definition:

```python
from toyaikit.tools import Tools

from toyaikit.chat import IPythonChatInterface
from toyaikit.chat.runners import OpenAIChatCompletionsRunner
from toyaikit.llm import OpenAIChatCompletionsClient

agent_tools = tools.AgentTools(Path(project_name))

tools_obj = Tools()
tools_obj.add_tools(agent_tools)

llm_client = OpenAIChatCompletionsClient(model='glm-4.5', client=zai_client)
chat_interface = IPythonChatInterface()

runner = OpenAIChatCompletionsRunner(
    tools=tools_obj,
    developer_prompt=developer_prompt,
    chat_interface=chat_interface,
    llm_client=llm_client
)
runner.run()
```

## Key Differences

Here we use:

- OpenAIChatCompletionsRunner instead of OpenAIResponsesRunner
- OpenAIChatCompletionsClient instead of OpenAIClient

These classes are compatible with the older chat completions API that Z.ai supports. The rest of the agent setup remains the same - you can use the same tools, prompts, and workflow.
