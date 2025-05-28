import os
import chainlit as cl

from agents import Agent, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

gemini_api_key =os.getenv("GEMINI_API_KEY")

# step 1: Provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Step 2:Model 
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

# step 3: Config defined at run level
run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

# step 3: Agent
agent1 = Agent(
    instructions="You ara a helpful Assistant that can Answer Question and  ",
    name= "Panaversity Support Agent"
)

# Step 5: Run
result= Runner.run_sync(
    agent1,
input="What is the capital of Pakistan?",
run_config= run_config,
# starting_agent=agent1
)

print(result.final_output)

@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello, I'm the Panaversity Support Agent. How can I help you?").send()


@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")

    history.append({"role": "user", "content": message.content})
    
    result = await Runner.run(
        agent1,
        input=history,
        run_config=run_config,
    )

    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)

    await cl.Message(content=result.final_output).send()
