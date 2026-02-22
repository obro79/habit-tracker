import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from agent.tools import ALL_TOOLS, TOOL_MAP

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
config = types.GenerateContentConfig(
    tools=ALL_TOOLS,
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)


async def handle_message(user_id: str, message: str) -> str:
    contents = [message]

    for _ in range(10):
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                config=config,
                contents=contents,
            )

            if (
                not response.candidates
                or not response.candidates[0].content.parts
            ):
                return "Sorry, I couldn't process that."

            part = response.candidates[0].content.parts[0]

            if part.function_call:
                func_name = part.function_call.name
                args = part.function_call.args

                tool_func = TOOL_MAP[func_name]
                result = await tool_func(user_id=user_id, **args)

                # Append result and loop so Gemini can call more tools
                contents.append(str(result))
            else:
                return response.text or ""

        except Exception as e:
            print(f"Error during tool execution: {e}")
            continue

    return "Sorry, too many tool calls."