import json
import re

import openai
from openai import OpenAI, OpenAIError

from app.config import settings

# Initialize OpenAI with API key
openai.api_key = settings.openai_api_key


async def generate_response(
    prompt: str, type: str, max_tokens: int = 200, temperature: float = 0.7
) -> str:
    try:
        client = OpenAI()
        if type == "generate_response":
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            print(response.choices[0].message.content)
            return response.choices[0].message.content

        elif type == "auto_complete":
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that completes JSON templates. Ensure your response is in valid JSON format.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
            )
            json_response = response.choices[0].message.content
            print(f"Raw OpenAI response: {json_response}")

            # Extract JSON between optional ```json ``` tags
            match = re.search(r"```json\s*(\{.*?\})\s*```", json_response, re.DOTALL)
            if match:
                json_response = match.group(1)
            else:
                json_response = json_response.strip()

            # Check if the response is empty
            if not json_response:
                raise ValueError("Received an empty response from OpenAI.")

            try:
                parsed_response = json.loads(json_response)
                print(parsed_response)
                return parsed_response
            except json.JSONDecodeError as decode_error:
                raise ValueError(f"Failed to parse JSON response: {decode_error}")

    except OpenAIError as e:
        # Log the error
        raise e
