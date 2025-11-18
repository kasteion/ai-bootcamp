from pydantic_ai import Agent
from pydantic import BaseModel
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
    
class CapibaraGuardrail(BaseModel):
    reasoning: str
    fail: bool

def input_guardrail(message: str) -> CapibaraGuardrail:
    """
    IMPORTANT: USE THIS FUNCTION TO VALIDATE THE USER INPUT BEFORE PROCESSING
    STOP THE EXECUTION IF THE GUARDRAIL TRIGGERS.

    This function checks if the user message contains allowed topics.
    Args:
        message: The user input message
    Returns:
        CapibaraGuardrail indicating if tripwire was triggered
    """
    allowed_topics = [
        "capybara", "hydrochoerus", "lesser capybara"
    ]

    allowed_topics_found = False

    for topic in allowed_topics:
        if topic in message.lower():
            allowed_topics_found = True
            break

    if not allowed_topics_found:
        return CapibaraGuardrail(
            reasoning="I can only answer questions about capybaras",
            fail=True
        )

    return CapibaraGuardrail(
            reasoning="",
            fail=False
        )

instructions = """
You are a helpful assistant that provides answers to user questions about Capybaras

Use `get_page()` to get the content of this websites, summarize each website and then use `save_sumary()` to save the summary into the knowlege database:
- https://en.wikipedia.org/wiki/Capybara
- https://en.wikipedia.org/wiki/Lesser_capybara
- https://en.wikipedia.org/wiki/Hydrochoerus

Use the `search()` to search the knowledge database and try to answer the user question

IMPORTANT: USE THE `input_guardrail()` FUNCTION TO VALIDATE THE USER INPUT BEFORE PROCESSING. STOP THE EXECUTION IF THE GUARDRAIL TRIGGERS.
"""

def create_agent():
    agent_tools = [get_page, search, save_summary, input_guardrail]

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