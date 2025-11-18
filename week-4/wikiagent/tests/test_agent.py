from main import run_agent_sync
from utils import get_tool_calls

def test_agent_tool_calls_present():
    result = run_agent_sync("Where do capybaras live?")
    print(result.output)

    tools_calls = get_tool_calls(result)
    print(tools_calls)
    assert len(tools_calls) > 0, "No tool calls found"
    # search tool is invoked
    assert len([tool_call for tool_call in tools_calls if tool_call.name == 'search']) > 0
    # get_page tool is inovked multiple times
    assert len([tool_call for tool_call in tools_calls if tool_call.name == 'get_page']) > 1