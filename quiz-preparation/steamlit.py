import os
import re
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from playwright.sync_api import sync_playwright  
import streamlit as st

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
    return filename

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
    return image_file

# --------------------
# AGENT SETUP
# --------------------
agent = Agent(
    name="Coder Agent | Developer Agent",
    instructions=(
        "You are a coding agent specialized in converting plain text into "
        "clean, semantic, and well-structured HTML code. "
        "Always return HTML wrapped in ```html code fences."
    ),
    model=model
)

# --------------------
# STREAMLIT APP
# --------------------
st.title("🖼️ AI HTML Generator with Screenshot")
prompt = st.text_area("Enter your prompt:", "Hello world in heading")

if st.button("Generate"):
    result = Runner.run_sync(agent, input=prompt)
    output = result.final_output

    st.subheader("🤖 Agent Output")
    st.code(output, language="html")

    # Extract HTML
    match = re.search(r"```html\n(.*?)```", output, re.DOTALL)
    if match:
        html_code = match.group(1).strip()
        html_file = save_html(html_code)
        image_file = html_to_image(html_file)

        # Show render + download
        st.subheader("🌐 Rendered HTML Page")
        st.components.v1.html(html_code, height=400, scrolling=True)

        st.subheader("📸 Screenshot")
        st.image(image_file)

        with open(image_file, "rb") as f:
            st.download_button("⬇️ Download Screenshot", f, file_name="screenshot.png")
    else:
        st.error("⚠️ No HTML code found in agent response")
