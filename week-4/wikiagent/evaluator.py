import json
import os
import asyncio
from typing import Dict, List, Any
from pydantic_ai import Agent


def load_logs(logs_dir: str) -> List[Dict[str, Any]]:
    """Load all JSON log files from the specified directory."""
    logs = []
    for filename in os.listdir(logs_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(logs_dir, filename)
            with open(filepath, 'r') as f:
                log = json.load(f)
                logs.append(log)
    return logs


def evaluate_followed_instructions(log: Dict[str, Any]) -> bool:
    """Evaluate if the agent followed the instructions."""
    messages = log.get('messages', [])
    instructions = log.get('system_prompt', [''])[0]  # Assuming first is the main

    # Check for required tool calls in order
    tool_calls = []
    for msg in messages:
        if msg.get('kind') == 'response':
            for part in msg.get('parts', []):
                if part.get('part_kind') == 'tool-call':
                    tool_calls.append(part.get('tool_name'))

    # Required sequence: get_page (multiple), save_summary (multiple), search
    # But in log, it did get_page, save_summary, no search
    # Instructions: get_page, save_summary, then search
    # So, check if get_page and save_summary are present, and search is used at some point

    has_get_page = 'get_page' in tool_calls
    has_save_summary = 'save_summary' in tool_calls
    has_search = 'search' in tool_calls

    # For this specific instructions, it should have all
    return has_get_page and has_save_summary and has_search


async def evaluate_answer_relevance(log: Dict[str, Any]) -> bool:
    """Evaluate if the answer is relevant to the user question."""

    agent = Agent(
        name="evaluator",
        instructions="You are an evaluator that checks if the answer is relevant to the user question. Answer with 'yes' or 'no'.",
        model="gpt-4o-mini",
    )

    output = log.get('output', '')
    user_question = None
    for msg in log.get('messages', []):
        if msg.get('kind') == 'request':
            for part in msg.get('parts', []):
                if part.get('part_kind') == 'user-prompt':
                    user_question = part.get('content')
                    break
        if user_question:
            break

    if not user_question or not output:
        return False

    # Use the agent to evaluate relevance
    response = await agent.run(f"User question: {user_question}\nAnswer: {output}\nIs the answer relevant to the user question? Answer with 'yes' or 'no'.")
    return 'yes' in response.output.lower()


async def evaluate_log(log: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate a single log."""
    followed = evaluate_followed_instructions(log)
    relevant = await evaluate_answer_relevance(log)
    return {
        'agent_name': log.get('agent_name'),
        'followed_instructions': followed,
        'answer_relevant': relevant,
        'overall_pass': followed and relevant
    }


async def main():
    logs_dir = './logs'
    logs = load_logs(logs_dir)
    evaluations = []
    for log in logs:
        eval_result = await evaluate_log(log)
        evaluations.append(eval_result)
        print(f"Evaluation for {eval_result['agent_name']}: Followed: {eval_result['followed_instructions']}, Relevant: {eval_result['answer_relevant']}, Pass: {eval_result['overall_pass']}")

    # Optionally, save evaluations to a file
    with open('./evaluations.json', 'w') as f:
        json.dump(evaluations, f, indent=2)


if __name__ == '__main__':
    asyncio.run(main())