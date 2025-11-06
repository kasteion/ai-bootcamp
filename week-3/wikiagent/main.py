import wikiagent
import asyncio
import sys

agent = asyncio.run(wikiagent.create_agent())
agent_callback = wikiagent.NamedCallback(agent)

async def run_agent(user_prompt: str):
    results = await agent.run(
        user_prompt=user_prompt,
        event_stream_handler=agent_callback
    )
    return results

def run_agent_sync(user_prompt: str):
    return asyncio.run(run_agent(user_prompt=user_prompt))

def main():
    if len(sys.argv) != 2:
        print("Usage main.py '<question>'")
        return
    
    user_prompt = sys.argv[1]
    result = run_agent_sync(user_prompt=user_prompt)
    print(result.output)

if __name__ == '__main__':
    main()