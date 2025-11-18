from pydantic import BaseModel

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