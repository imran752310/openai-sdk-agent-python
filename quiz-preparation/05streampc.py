from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
import os
import asyncio

from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
Bas_url = os.environ.get("BASE_URL")

if not api_key:
    raise ValueError("api errror")

set_tracing_disabled(True)

client = AsyncOpenAI(
    api_key= api_key,
    base_url=Bas_url
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

agent = Agent(
    name="Joke",
    instructions="you are  best joker agent",
    model=model
)

async def main():

    result = Runner.run_streamed(agent, input="write 5 joke" )

    async for event in result.stream_events():
        print(event)
        print("================================ \n\n")
        # if event.type =="raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
        #     print(event.data.delta, end="", flush=True)

if __name__== "__main__":
    asyncio.run(main())



