from agents import Agent,handoff , Runner,RunContextWrapper ,OpenAIChatCompletionsModel, set_tracing_disabled, AsyncOpenAI,input_guardrail,output_guardrail,GuardrailFunctionOutput, OutputGuardrailTripwireTriggered
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

from pydantic import BaseModel

load_dotenv()
set_tracing_disabled(False)
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

urduAgent = Agent(
    name="Urdu Translator",
    instructions="you always translate the user query in urdu language",
    model=model,
)


spanishagent = Agent(
    name="Spanish Translator",
    instructions="you always translate the user query in spainsh language",
    model=model,
)

class EscilatonData(BaseModel):
        reson: str
        language: str

def on_urdu(ctx:RunContextWrapper):
    print("\n transfering to Urdu agent  \n")
    
def on_spanishagent(ctx:RunContextWrapper, input: EscilatonData):
    print( f"\n transfering to spanish agent {input.reson}, {input.language} \n")

mainagent = Agent(
    name="Main Agent",
    instructions="you are the main agent that can transfer the query query into coresponding agent",
    model=model,
    # tools=[spanishagent.as_tool(
    #     tool_name="spanish_tarnslator",
    #     tool_description="you are spnish translator"
    # ), urduAgent.as_tool(
    #     tool_name="urdu_translator",
    #     tool_description="your are urdu translator"
    # )]
     handoffs=[handoff(spanishagent, on_handoff=on_spanishagent, input_type=EscilatonData), handoff(urduAgent, on_handoff=on_urdu)]
)

result = Runner.run_sync(
    mainagent, 
    input="i am a develper translate in spnaish"
)

print(result.final_output)
print(result.last_agent.name)