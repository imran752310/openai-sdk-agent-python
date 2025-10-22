from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled
import os
from dotenv import load_dotenv


load_dotenv()
set_tracing_disabled(True)

apikey = os.environ.get("GEMINI_API_KEY")
BasUrl = os.environ.get("BASE_URL")

client = AsyncOpenAI(
    api_key=apikey,
    base_url=BasUrl
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client= client
)

agent = Agent(
    name="Hotel booking agent",
    instructions="your are a  Hotel booking agent you search for hotel and near by place",
    model= model
)


session = SQLiteSession(
    session_id = "imran",
    db_path= "test.db"
)

while True :
    user_input = input("how i can help you")
    if user_input == "q":
        break
    Result = Runner.run_sync(
    agent,
    input=  user_input,
    session= session,
    )
    print(Result.final_output)

