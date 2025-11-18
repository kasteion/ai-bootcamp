import wikiagent
import asyncio
import sys

from agent_logging import log_streamed_run, save_log


# async def run_agent(user_prompt: str):
#     results = await agent.run(
#         user_prompt=user_prompt,
#         event_stream_handler=agent_callback
#     )
#     return results

# def run_agent_sync(user_prompt: str):
#     return asyncio.run(run_agent(user_prompt=user_prompt))

async def main():
    if len(sys.argv) != 2:
        print("Usage main.py '<question>'")
        return
    
    user_prompt = sys.argv[1]

    agent = wikiagent.create_agent()
    callback = wikiagent.NamedCallback(agent)

    previous_text = ""

    async with agent.run_stream(user_prompt, event_stream_handler=callback) as result:
        async for item, last in result.stream_responses(debounce_by=0.01):
            for part in item.parts:
                if not hasattr(part, "tool_name"):
                    continue
                if part.tool_name != "final_result":
                    continue

                current_text = part.args
                delta = current_text[len(previous_text):]
                print(delta, end="", flush=True)
                previous_text = current_text

    log_entry = await log_streamed_run(agent, result)
    save_log(log_entry)
    print(log_entry['output'])

if __name__ == '__main__':
    asyncio.run(main())