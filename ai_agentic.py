import os
from openai import OpenAI
from dotenv import load_dotenv
from engine import assign_resources, detect_conflicts, urgent_reassignment

load_dotenv()
client = OpenAI()

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "assign_resources",
            "description": "Assign pilot and drone to mission",
            "parameters": {
                "type": "object",
                "properties": {
                    "mission_id": {"type": "string"}
                },
                "required": ["mission_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "detect_conflicts",
            "description": "Detect scheduling conflicts",
            "parameters": {
                "type": "object",
                "properties": {
                    "mission_id": {"type": "string"}
                },
                "required": ["mission_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "urgent_reassignment",
            "description": "Handle urgent mission reassignment",
            "parameters": {
                "type": "object",
                "properties": {
                    "mission_id": {"type": "string"}
                },
                "required": ["mission_id"]
            }
        }
    }
]


def chat_with_agent(user_message):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a Drone Operations AI Agent."},
            {"role": "user", "content": user_message}
        ],
        tools=TOOLS,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        function_name = tool_call.function.name
        args = eval(tool_call.function.arguments)

        if function_name == "assign_resources":
            result = assign_resources(**args)
        elif function_name == "detect_conflicts":
            result = detect_conflicts(**args)
        elif function_name == "urgent_reassignment":
            result = urgent_reassignment(**args)
        else:
            result = {"error": "Unknown function"}

        return result

    return {"message": message.content}
