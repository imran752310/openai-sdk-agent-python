import os
import re
import chainlit as cl
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from playwright.sync_api import sync_playwright  

# --------------------
# ENV + CLIENT SETUP
# --------------------
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ No GEMINI_API_KEY found in .env file")

set_tracing_disabled(True)

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client,
)

def save_html(html_code: str, filename="output.html"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_code)
    return filename

def html_to_image(html_file="output.html", image_file="screenshot.png"):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file:///{os.path.abspath(html_file)}")
        page.screenshot(path=image_file, full_page=True)
        browser.close()
    return image_file

agent = Agent(
    name="Coder Agent | Developer Agent",
    instructions="Convert plain text into HTML inside ```html fences.",
    model=model
)

@cl.on_message
async def main(message: cl.Message):
    result = Runner.run_sync(agent, input=message.content)
    output = result.final_output

    await cl.Message(content="🤖 Generated Code:\n" + output).send()

    match = re.search(r"```html\n(.*?)```", output, re.DOTALL)
    if match:
        html_code = match.group(1).strip()
        html_file = save_html(html_code)
        image_file = html_to_image(html_file)

        await cl.Message(content="🌐 Rendered HTML:", elements=[
            cl.Html(name="render", content=html_code)
        ]).send()

        await cl.Message(content="📸 Screenshot:", elements=[
            cl.Image(name="screenshot", path=image_file)
        ]).send()
