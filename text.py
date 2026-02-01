"""Module for sending text notifications about unchecked habits."""

import os
from twilio.rest import Client
from google import genai
from gemini_prompt import TEXT_PROMPT
from dotenv import load_dotenv

load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")
client = Client(account_sid, auth_token)


def send_text_notification(habits: dict):
    """Sends a text notification listing unchecked habits for today.

    Args:
        habits (dict): A dict where keys are habit names and vals are bools
                       indicating whether the habit was checked off today.
    """
    message_body = get_gemini_response()
    message = client.messages.create(
        body=message_body, from_=twilio_number, to=os.getenv("MY_NUMBER", "")
    )

    print(f"Notification sent with SID: {message.sid}")


def get_gemini_response() -> str:
    """Gets a response from the Gemini API for the given prompt.

    Args:
        prompt (str): The prompt to send to the Gemini API."""
    tasks = ""

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", ""))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=TEXT_PROMPT + f"{tasks}",
    )
    return response.text or "Error: No response from Gemini API"


if __name__ == "__main__":
    send_text_notification({})
