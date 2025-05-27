!pip install -Uq openai-agents

import nest_asyncio
nest_asyncio.apply()

BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "thudm/glm-z1-32b:free"

import requests
import json

response = requests.post(
  url=f"{BASE_URL}/chat/completions",
  headers={
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
  },
  data=json.dumps({
    "model": MODEL,
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ]
  })
)

print(response.json())


data = response.json()
data['choices'][0]['message']['content']


## Using OpenAI Agents SDK

import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled

client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL
)

set_tracing_disabled(disabled=True)

async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="tell about palastain.",
        model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
    )

    result = await Runner.run(
        agent,
        "country name and capital.",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())


