from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled

from dotenv   import load_dotenv
import os

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("plase value error");

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
    name="assistant agent",
    instructions="your are` best greeting agent",
    model=model
)

result = Runner.run_sync(
    agent,
    "your hi"
)
print(result.final_output)