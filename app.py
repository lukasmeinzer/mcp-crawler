import streamlit as st
import asyncio
from firebase_agent import run_agent
import traceback 

st.set_page_config(page_title="scrapy ai", layout="wide")

st.title("WebCrawling Agent  'scrapy_ai' (Firecrawl + MCP)")
st.subheader("(läuft solange das Geld reicht 👀)")

# Initialize session state for conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_prompt = st.chat_input("Ask something to crawl the web...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")

    async def get_response():
        try:
            # Use your existing crawling logic or a wrapped function
            result = await run_agent(user_prompt)
            return result
        except Exception as e:
            traceback.print_exc()  # prints full traceback to stderr
            return f"Error: {e}"

    # Run the async function and get the result
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(get_response())
    loop.close()

    message_placeholder.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
