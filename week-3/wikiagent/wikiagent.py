from pydantic_ai import Agent
from tools import get_page, search, save_summary
from pydantic_ai.messages import FunctionToolCallEvent

class NamedCallback:
    def __init__(self, agent):
        self.agent_name = agent.name

    async def print_function_calls(self, ctx, event):
        # Detect nested streams
        if hasattr(event, "__aiter__"):
            async for sub in event:
                await self.print_function_calls(ctx, sub)
            return

        if isinstance(event, FunctionToolCallEvent):
            tool_name = event.part.tool_name
            args = event.part.args
            print(f"TOOL CALL ({self.agent_name}): {tool_name}({args})")

    async def __call__(self, ctx, event):
        return await self.print_function_calls(ctx, event)

instructions = """
You are a helpful assistant that provides answers to user questions about Capybaras

Use `get_page()` to get the content of this websites, summarize each website and then use `save_sumary()` to save the summary into the knowlege database:
- https://en.wikipedia.org/wiki/Capybara
- https://en.wikipedia.org/wiki/Lesser_capybara
- https://en.wikipedia.org/wiki/Hydrochoerus

Use the `search()` to search the knowledge database and try to answer the user question
"""

async def create_agent():
    agent_tools = [get_page, search, save_summary]

    agent = Agent(
        name='wikiagent',
        instructions=instructions,
        tools=agent_tools,
        model='gpt-4o-mini'
    )

    # await agent.run(
    #     user_prompt="Summarize https://en.wikipedia.org/wiki/Capybara",
    #     event_stream_handler=NamedCallback(agent)
    # )

    # await agent.run(
    #     user_prompt="Summarize https://en.wikipedia.org/wiki/Lesser_capybara",
    #     event_stream_handler=NamedCallback(agent)
    # )

    # await agent.run(
    #     user_prompt="Summarize https://en.wikipedia.org/wiki/Hydrochoerus",
    #     event_stream_handler=NamedCallback(agent)
    # )

    return agent