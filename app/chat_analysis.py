# Import Dependencies
import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Optional

load_dotenv()
#openai.api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

OPENAI_MODEL = os.environ.get(
    "OPENAI_MODEL",
    "gpt-5.5",
)

USER_LABEL = "You:"
BOT_LABEL = "Jabe:"

SYSTEM_INSTRUCTIONS = (
    "You are Jabe, a fictional chatbot influencer. "
    "Jabe has a humorous and entertaining personality, creates memes, "
    "publishes online videos, and sells merchandise. "
    "Stay in character as Jabe while remaining helpful and appropriate."
)

SESSION_PROMPT = (
    "You are talking to Jabe, a GPT chatbot influencer."
    "Jabe has a humorous and entertaining personality, creates memes, "
    "publishes online videos, and sells merchandise. "
    "Stay in character as Jabe while remaining helpful and appropriate."
)


def ask(question: str, chat_log: Optional[str] = None) -> str:
    """
    Send the current conversation to the OpenAI API and return the bot's answer.
    """

    if not question or not question.strip():
        return "Please enter a message."

    current_log = chat_log or SESSION_PROMPT

    prompt_text = (
        f"{current_log.rstrip()}\n\n"
        f"{USER_LABEL} {question.strip()}\n"
        f"{BOT_LABEL}"
    )

    try:
        response = client.responses.create(
                model=OPENAI_MODEL,
                instructions=SYSTEM_INSTRUCTIONS,
                input=prompt_text,
        )

        answer = response.output_text.strip()
        
        if not answer:
            return "I could not generate a response. Please try again."

        return answer
    
    except Exception as error:
        print(f"OpenAI API error: {error}")
        return "The chatbot is temporarily unavailable. Please try again."


def append_interaction_to_chat_log(
    question: str,
    answer: str,
    chat_log: Optional[str] = None,
) -> str:
    """
    Add one user-and-bot exchange with consistent blank-line spacing.
    """

    current_log = chat_log or SESSION_PROMPT

    return (
        f"{current_log.rstrip()}\n\n"
        f"{USER_LABEL} {question.strip()}\n\n"
        f"{BOT_LABEL} {answer.strip()}"
    )