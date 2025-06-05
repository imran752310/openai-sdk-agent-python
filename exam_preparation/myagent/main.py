import os
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
from agents.run import RunConfig
from dotenv import load_dotenv

load_dotenv()

Groq_api = os.getenv("GROQ_API")
Baseurl = os.getenv("BASE_URL")

# Set up the client for OpenAI-compatible models
Provider = AsyncOpenAI(
    api_key=Groq_api,
    base_url=Baseurl,
)

# Define the model (make sure it's one Groq supports, like mixtral-8x7b)
model = OpenAIChatCompletionsModel(
    model="mixtral-8x7b-32768",  # or another supported model name
    openai_client=Provider,
)
config = RunConfig(
    tracing_disabled=True,
    model_provider=model,  # this is correct
)
agent = Agent(
    name="Agent",
    instructions="You are a helpful assistant.",
)



result = Runner.run_sync(
    agent,
    input="What is the capital of Swat?",
    run_config=config,
)


print(result.final_output)
