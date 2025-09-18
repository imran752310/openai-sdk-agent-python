from agents import Agent,Runner ,set_default_openai_api,set_default_openai_client , AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api = os.environ.get("GEMINI_API_KEY")

if not api:
    raise ValueError("api key error")



client = AsyncOpenAI(
    api_key=api,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/" 
)

set_default_openai_api("chat_completions")
set_default_openai_client(client)

agent = Agent(
    name="teacher agent",
    instructions="your are best teacher agent you solve every question",
     model="gemini-2.5-flash"
)

result = Runner.run_sync(
    agent,
    "what is math "
)
print(result.final_output)