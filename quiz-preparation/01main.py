from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
import os
import re

# For screenshot rendering (install: pip install playwright)
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

# --------------------
# SAVE HTML FUNCTION
# --------------------
def save_html(html_code: str, filename="output.html"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_code)
    print(f"✅ HTML saved as {filename}")

# --------------------
# CONVERT HTML TO IMAGE
# --------------------
def html_to_image(html_file="output.html", image_file="screenshot.png"):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file:///{os.path.abspath(html_file)}")
        page.screenshot(path=image_file, full_page=True)
        browser.close()
    print(f"📸 Screenshot saved as {image_file}")

# --------------------
# AGENT SETUP
# --------------------
agent = Agent(
    name="Coder Agent | Developer Agent",
    instructions=(
        "You are a coding agent specialized in converting plain text into "
        "clean, semantic, and well-structured HTML code. "
        "Your role is to act as a professional developer who: \n"
        "- Always outputs valid HTML5 code wrapped with proper tags. \n"
        "- Uses semantic HTML elements (e.g., <h1>, <p>, <ul>, <li>, <div>, <span>, <section>). \n"
        "- Ensures indentation and formatting for readability. \n"
        "- Avoids unnecessary inline styles unless explicitly requested. \n"
        "- If user provides plain text, generate HTML code representing that content. \n"
        "- If user specifies formatting (like headings, paragraphs, lists, bold, italics), apply correct HTML tags. \n"
        "- Always enclose your response inside ```html code fences for clarity. \n"
        "Example:\n"
        "Input: 'Hello world in heading'\n"
        "Output:\n"
        "```html\n<h1>Hello world</h1>\n```"
        "After writing code, convert it into an HTML page and save it."
    ),
    model=model
)

# --------------------
# RUN AGENT
# --------------------
user_prompt = input("Enter your prompt: ")

result = Runner.run_sync(
    agent,
    input=user_prompt
)

output = result.final_output
print("\n🤖 Agent Output:\n", output)

# --------------------
# EXTRACT HTML FROM RESPONSE
# --------------------
match = re.search(r"```html\n(.*?)```", output, re.DOTALL)
if match:
    html_code = match.group(1).strip()
    save_html(html_code, "output.html")
    html_to_image("output.html", "screenshot.png")
else:
    print("⚠️ No HTML code found in agent response")



# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled

# from dotenv   import load_dotenv
# import os

# load_dotenv()
# api_key = os.environ.get("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("plase value error");

# set_tracing_disabled(True)

# client = AsyncOpenAI(
#     api_key=api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    

# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.5-flash",
#     openai_client=client,
  
  
# )

# agent = Agent(
#     name="Coder Agent | Developer Agent",
#     instructions=(
#         "You are a coding agent specialized in converting plain text into "
#         "clean, semantic, and well-structured HTML code. "
#         "Your role is to act as a professional developer who: \n"
        
#         "- Always outputs valid HTML5 code wrapped with proper tags. \n"
#         "- Uses semantic HTML elements (e.g., <h1>, <p>, <ul>, <li>, <div>, <span>, <section>). \n"
#         "- Ensures indentation and formatting for readability. \n"
#         "- Avoids unnecessary inline styles unless explicitly requested. \n"
#         "- If user provides plain text, generate HTML code representing that content. \n"
#         "- If user specifies formatting (like headings, paragraphs, lists, bold, italics), "
#         "apply correct HTML tags. \n"
#         "- Always enclose your response inside ```html code fences for clarity. \n"
#         "Example:\n"
#         "Input: 'Hello world in heading'\n"
#         "Output:\n"
#         "```html\n<h1>Hello world</h1>\n```"
#         "after write code then Convert it into html page"
#     ),
#     model=model
# )

# result = Runner.run_sync(
#     agent,
#     input = input("enter your prompt ")
# )
# print(result.final_output)