from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
import asyncio
import os
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
tavily_api = os.environ.get("TAVILY_API")

if not api_key:
    raise ValueError("Please provide GEMINI_API_KEY")
if not tavily_api:
    raise ValueError("Please provide TAVILY_API")

set_tracing_disabled(True)

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client,
)

agent = Agent(
    name="Joker",
    instructions="You are a helpful assistant.",
    model=model
)

async def main():
    
    result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")

    
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())

