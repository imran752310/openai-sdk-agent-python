import asyncio
from dataclasses import dataclass
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, function_tool,ModelSettings,RunContextWrapper
from dotenv import load_dotenv
import os

set_tracing_disabled(True)
load_dotenv()
api = os.environ.get("GEMINI_API_KEY")
base_url = os.environ.get("BASE_URL")

client = AsyncOpenAI(
    api_key=api,
    base_url=base_url,
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.5-flash",
)
@function_tool("piaic_student_finder")
def piaic_student_finder(student_roll: int) -> str:
  """
  find the PIAIC student based on the roll number
  """
  data = {1: "Ammar",
          2: "Azeem",
          3: "Zain"}

  return data.get(student_roll, "Not Found") # Azeem

@dataclass
class UserContext:
   
   username: str
   email: str | None =None


@function_tool("get_weather")
def get_weather(name:str, unit:str) -> str:
    """this is get weather tool"""
    return"the {name} is very sanny degree {unit}"

@function_tool
async def search(local_context: RunContextWrapper[UserContext], query: str) -> str:
   
    import time
    time.sleep(30)  # Simulating a delay for the search operation
    return "No results found."

async def special_prompt(spacial_context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
   
    print(f"\nUser: {spacial_context.context},\n Agent: {agent.name}\n")
    return f"You are a math expert. User: {spacial_context.context.username}, Agent: {agent.name}. Please assist with math-related queries."

agent = Agent(
    name="Helping Agent | weather agent | Student Finding Agent",
    instructions=special_prompt,
    tools=[get_weather,piaic_student_finder],
    model=model,
        model_settings=ModelSettings(
        temperature=0, 
        max_tokens=1024,
        top_p=1,
        tool_choice="required"
    )
)

# result = Runner.run_sync(
#     agent,
#     input=input("enter your prompt : ")
# )
# print(result.final_output)


async def call_agent():
    # Call the agent with a specific input
    user_context = UserContext(username="abdullah")

    output = await Runner.run(
        starting_agent=get_weather, 
        input="search for the best math tutor in my area",
        context=user_context
        )
    print(f"\n\nOutput: {output.final_output}\n\n")
    
asyncio.run(call_agent())
