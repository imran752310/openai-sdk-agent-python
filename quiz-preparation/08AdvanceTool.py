from agents import Agent, Runner,RunContextWrapper ,OpenAIChatCompletionsModel, set_tracing_disabled, AsyncOpenAI,function_tool
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

from pydantic import BaseModel

load_dotenv()
set_tracing_disabled(True)
apikey = os.environ.get("GEMINI_API_KEY")
base_url = os.environ.get("BASE_URL")

client = AsyncOpenAI(
    api_key=apikey,
    base_url=base_url
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)
class UserContext(BaseModel):
    username: str
    is_admin: bool
    tool_allow: bool

def is_post_allowed(ctx:RunContextWrapper[UserContext], agent: Agent):
    # return True if ctx.context.tool_allow else False
  
   if ctx.context.tool_allow:
       return True 
   else:
       return False
   


    

@function_tool(name_override="post_creatton", description_override="post creating tool", is_enabled=is_post_allowed)
def Create_Post(ctx:RunContextWrapper[UserContext],  description:str):
    print("\n Post Tool Calling \n")
    if ctx.context.is_admin: 

        return f"your post {description} is created"
    else:
       
        return "you are not Allowed"


agentool =Agent(
    name="Base Agent",
    instructions="Your are a helpfull assistent",
    model=model,
    tools=[Create_Post]
)

userdata = UserContext(username="mustafa", is_admin=True, tool_allow=True)

result= Runner.run_sync(
    agentool,
    input="hi create a post for agentic ai",
    context=userdata
)

print(result.final_output)
