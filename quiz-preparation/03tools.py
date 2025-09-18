from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool,set_tracing_disabled, ModelSettings
from tavily import TavilyClient
from dotenv   import load_dotenv
import os

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
tavily_api = os.environ.get("TAVILY_API")

tavily_client = TavilyClient(api_key=tavily_api)

if not api_key:
    raise ValueError("plase value error")
if not tavily_api:
    raise ValueError("plase value tavilt error")

set_tracing_disabled(True)

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client,
)

# @function_tool
# def math_Calculation(numbers: str) -> str :
#     """this is the math Tool : you do multiplication and addition """
#     return f"the calculation is {numbers} "
    
# @function_tool
# def get_weather(location:str) -> str :
#     """use this tools for weather"""

#     return f"The {location} is very good saunny "

# @function_tool
# def web_Search(query: str) -> str :
#     """This is Web Search"""
#     response = tavily_client.search(query=query)
#     print("\n[Tavily Response] ", response)
#     return response

# agent = Agent(
#     name="Travel Agent",
#     instructions="your are   Travel agent , and mathimatical agent calculation agent",
#     model=model,
#     tools=[web_Search]
# )

# result = Runner.run_sync(
#     agent,
#     input=input("enter your question")
# )
# print(result.final_output)



@function_tool("weather_tool")
def weather_tool(location: str, unit: str) -> str:
  """
  Fetch the weather for a given location, returning a short description.
  """
  return f"The weather in {location} is 22 degrees {unit}."


@function_tool("calculator")
def calculator(a: float, b: float) -> float:
    """
    Add two numbers and return the result.
    """
    return a + b

# Agent can decide when to use tools (default)
agent_auto = Agent(
    name="Smart Assistant",
    instructions="You are a helpful assistant.",
    model=model,
    tools=[calculator, weather_tool],
    model_settings=ModelSettings(tool_choice="auto")
)

result_auto = Runner.run_sync(
    agent_auto,
    input="What is the weather in Karachi in Celsius?"
)
print("Auto tool choice:", result_auto.final_output)

# Agent MUST use a tool (even if not needed)
agent_required = Agent(
    name="Tool User",
    instructions="You are a helpful assistant.",
    model=model,
    tools=[calculator, weather_tool],
    model_settings=ModelSettings(tool_choice="required")
)

result_required = Runner.run_sync(
    agent_required,
    input="What is the weather in Karachi in Celsius?"
)
print("Required tool choice:", result_required.final_output)

# Agent CANNOT use tools (chat only)
agent_no_tools = Agent(
    name="Chat Only",
    instructions="You are a helpful assistant.",
    model=model,
    tools=[calculator, weather_tool],
    model_settings=ModelSettings(tool_choice="none")
)

result_no_tools = Runner.run_sync(
    agent_no_tools,
    input="What is the weather in Karachi in Celsius?"
)
print("No tool choice:", result_no_tools.final_output)
