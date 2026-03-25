import asyncio
import os
import re
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from graph.graph import graph

# Page Configuration
st.set_page_config(
    page_title="Brand Boost AI Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a premium feel
st.markdown("""
<style>
    .main {
        background-color: #f9f9f9;
    }
    .stChatMessage {
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .stChatMessage[data-testimonial="user"] {
        background-color: #ffffff;
        border-left: 5px solid #007BFF;
    }
    .stChatMessage[data-testimonial="assistant"] {
        background-color: #f0f2f6;
        border-left: 5px solid #6c757d;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1E1E1E;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .sidebar-content {
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/rocket.png", width=120)
    st.title("🚀 Brand Boost AI")
    st.markdown("---")
    
    if st.button("✨ Start New Campaign", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.display_history = []
        st.rerun()
    
    st.markdown("### 💡 Try these ideas:")
    suggestions = [
        "Create a logo for my bakery",
        "Domain ideas for AI SaaS",
        "Marketing plan for a gym",
        "SEO keywords for tech blog"
    ]
    for s in suggestions:
        st.markdown(f"- {s}")

    st.markdown("---")
    st.caption("Powered by AWS Bedrock + LangGraph")

# Main Title Area (only show if no history)
if not st.session_state.get("display_history"):
    st.markdown("# Welcome to Brand Boost AI")
    st.markdown("#### I am Your personal AI Marketing Agency. Let's build your brand together.")
    st.info("👋 Tell me about your business name and what you do to get started!")
else:
    st.markdown("### 🚀 Brand Boost AI Campaign")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "display_history" not in st.session_state:
    st.session_state.display_history = []


def _render_extras(extras: dict):
    """Render logo image based on flags."""
    if extras.get("show_logo") and extras.get("logo_path"):
        logo_path = extras["logo_path"]
        if os.path.exists(logo_path):
            with st.expander("🎨 View Generated Visuals", expanded=True):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(logo_path, caption="Logo Concept", use_container_width=True)
                with col2:
                    st.success("Design Completed!")
                    st.write(f"**Saved to:** `{logo_path}`")
                    with open(logo_path, "rb") as f:
                        st.download_button(
                            label="Download PNG",
                            data=f,
                            file_name=os.path.basename(logo_path),
                            mime="image/png"
                        )


for role, content in st.session_state.display_history:
    with st.chat_message(role):
        if isinstance(content, dict):
            st.markdown(content["text"])
            _render_extras(content)
        else:
            st.markdown(content)


async def run_agent_stream(messages):
    """Stream tokens from the graph using astream_events."""
    full_response = ""
    with st.chat_message("assistant"):
        placeholder = st.empty()
        status_box = st.empty()

        async for event in graph.astream_events(
            {"messages": messages},
            version="v2",
        ):
            kind = event["event"]

            # Token-level streaming from the LLM inside the agent node
            if kind == "on_chat_model_stream":
                chunk = event["data"]["chunk"]
                content = chunk.content

                # content can be str or list of content blocks
                if isinstance(content, list):
                    text = "".join(
                        block.get("text", "") if isinstance(block, dict) else str(block)
                        for block in content
                    )
                else:
                    text = content or ""

                # Skip tool-call-only chunks (no text)
                if text:
                    full_response += text
                    placeholder.markdown(full_response + " ▌")

            # Show tool execution status
            elif kind == "on_tool_start":
                tool_name = event.get("name", "tool")
                status_box.status(f"🛠️ Running: ...", expanded=False)

        status_box.empty()
        placeholder.markdown(full_response)
    return full_response


# Handle input
if input_prompt := st.chat_input("Ask about domains, logos, strategy..."):
    st.chat_message("user").markdown(input_prompt)
    st.session_state.display_history.append(("user", input_prompt))

    st.session_state.messages.append(HumanMessage(content=input_prompt))

    full_response = asyncio.run(run_agent_stream(st.session_state.messages))

    answer_lower = full_response.lower()
    show_logo = "logo" in answer_lower and ("generated" in answer_lower or "saved" in answer_lower)

    # Extract logo path if generated
    logo_path = None
    if show_logo:
        # Match something like "generated_logos/My_Business_logo.png"
        match = re.search(r"generated_logos[/\\][\w\s.-]+_logo\.png", full_response)
        if match:
            logo_path = match.group(0)

    extras = {"show_logo": show_logo, "logo_path": logo_path}
    if show_logo:
        with st.chat_message("assistant"):
            _render_extras(extras)

    st.session_state.messages.append(AIMessage(content=full_response))

    st.session_state.display_history.append(
        ("assistant", {"text": full_response, **extras})
    )
