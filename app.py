import asyncio
import re
from dotenv import load_dotenv
import streamlit as st
from streamlit_option_menu import option_menu
from langchain_core.messages import HumanMessage, AIMessage
from graph.graph import graph
from supabase_utils import get_supabase_client, sign_in, sign_up, sign_out, create_conversation, get_user_conversations, add_message, get_conversation_messages

load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="Brand Boost AI Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Supabase Client in Session State
if "supabase" not in st.session_state:
    st.session_state.supabase = get_supabase_client()

# Initialize Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"  
if "current_conversation_id" not in st.session_state:
    st.session_state.current_conversation_id = None
if "business_name" not in st.session_state:
    st.session_state.business_name = "N/A"
if "display_history" not in st.session_state:
    st.session_state.display_history = []

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #f9f9f9; }
    .stChatMessage { border-radius: 12px; padding: 15px; margin-bottom: 10px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
    .stButton>button { border-radius: 8px; font-weight: 600; text-transform: uppercase; }
    .hero-section { text-align: center; padding: 50px 0; background: linear-gradient(135deg, #007BFF 0%, #00d4ff 100%); color: white; border-radius: 15px; margin-bottom: 30px; }
    .feature-card { padding: 20px; border-radius: 10px; background: white; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center; }
    
    /* Hide the link/anchor icons next to headers */
    header a, h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Navigation
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/rocket.png", width=120)
    st.title("🚀 Brand Boost AI")
    
    if st.session_state.logged_in and st.session_state.user:
        st.write(f"Logged in as: **{st.session_state.user.email}**")
        if st.button("Logout", key="logout_btn"):
            sign_out(st.session_state.supabase)
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.current_page = "Home"
            # Fully reset everything
            st.session_state.messages = []
            st.session_state.current_conversation_id = None
            st.session_state.business_name = "N/A"
            st.session_state.display_history = []
            st.rerun()
        
        menu_options = ["Home", "Chatbot"]
        menu_icons = ["house", "chat-dots"]
    else:
        menu_options = ["Home", "Login"]
        menu_icons = ["house", "box-arrow-in-right"]

    # Calculate default index based on current_page to keep sidebar in sync
    try:
        default_index = menu_options.index(st.session_state.current_page)
    except ValueError:
        default_index = 0

    selected = option_menu(
        menu_title=None,
        options=menu_options,
        icons=menu_icons,
        default_index=default_index,
    )
    st.session_state.current_page = selected

# --- PAGE: HOME ---
def show_home():
    st.markdown("""
    <div class="hero-section">
        <h1>Welcome to Brand Boost AI</h1>
        <p style="font-size: 1.2rem;">Your personal AI-powered Marketing Agency. Build your brand, grow your business.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎨 Visual Branding</h3>
            <p>Generate professional logos instantly with our AI Logo Agent.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📈 Marketing Strategy</h3>
            <p>Develop data-driven marketing plans tailored to your business goals.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍 SEO & Domain</h3>
            <p>Find the perfect domain name and optimize your online presence.</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="feature-card">
            <h3>🛡️ Competitor Analysis</h3>
            <p>Analyze rivals and differentiate your brand with AI-driven insights.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    if not st.session_state.logged_in:
        st.info("👋 Get started by logging in or signing up!")
        if st.button("Get Started Now", type="primary"):
            st.session_state.current_page = "Login"
            st.rerun()
    else:
        st.success(f"Welcome back, {st.session_state.user.email}! Ready to boost your brand?")
        if st.button("Open Chatbot", type="primary"):
            st.session_state.current_page = "Chatbot"
            st.rerun()

# --- PAGE: LOGIN/SIGNUP ---
def show_login():
    st.title("🔐 Authentication")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                try:
                    # Use a fresh client for login to avoid any cross-session pollution
                    temp_supabase = get_supabase_client()
                    res = sign_in(temp_supabase, email, password)
                    
                    # Store THIS user's client and info
                    st.session_state.supabase = temp_supabase
                    st.session_state.logged_in = True
                    st.session_state.user = res.user
                    
                    # Force reset of all conversation-related state
                    st.session_state.messages = []
                    st.session_state.current_conversation_id = None
                    st.session_state.business_name = "N/A"
                    st.session_state.current_page = "Home"
                    
                    st.success("Successfully logged in!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {e}")
    
    with tab2:
        with st.form("signup_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign Up")
            if submitted:
                try:
                    res = sign_up(st.session_state.supabase, email, password)
                    st.success("Signup successful! You can now switch to the Login tab and sign in.")
                except Exception as e:
                    st.error(f"Signup failed: {e}")

# --- PAGE: CHATBOT ---
async def show_chatbot():
    if not st.session_state.logged_in or st.session_state.user is None:
        st.warning("Please login to access the chatbot.")
        return

    st.title("💬 Brand Boost Assistant")
    
    # Sidebar for conversation history
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🕒 Recent Campaigns")
        
        # Double check user ID is present
        user_id = st.session_state.user.id
        conversations = get_user_conversations(st.session_state.supabase, user_id)
        
        if st.button("✨ Start New Campaign", use_container_width=True, type="primary"):
            st.session_state.current_conversation_id = None
            st.session_state.messages = []
            st.rerun()
            
        for conv in conversations:
            if st.button(f"📄 {conv['title']}", key=f"conv_{conv['id']}", use_container_width=True):
                st.session_state.current_conversation_id = conv['id']
                # Load messages
                msgs = get_conversation_messages(st.session_state.supabase, conv['id'])
                st.session_state.messages = []
                for m in msgs:
                    if m['role'] == 'user':
                        st.session_state.messages.append(HumanMessage(content=m['content']))
                    else:
                        st.session_state.messages.append(AIMessage(content=m['content'], response_metadata={"extras": m['extras']}))
                st.rerun()

    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History
    for msg in st.session_state.messages:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(msg.content)
            # Display extras (logos, etc.)
            if hasattr(msg, "response_metadata") and "extras" in msg.response_metadata:
                extras = msg.response_metadata["extras"]
                if "logo_url" in extras:
                    st.image(extras["logo_url"], width=300)

    # Chat Input
    if prompt := st.chat_input("How can I help you today?"):
        # Create conversation if not exists
        if st.session_state.current_conversation_id is None:
            # Extract business name from prompt if possible (simple regex)
            business_match = re.search(r"my (?:business|company|bakery|gym|shop) (?:is|is called) ([\w\s]+)", prompt, re.IGNORECASE)
            business_name = business_match.group(1).strip() if business_match else "New Campaign"
            title = business_name if business_name != "New Campaign" else prompt[:30] + "..."
            st.session_state.current_conversation_id = create_conversation(st.session_state.supabase, st.session_state.user.id, title, business_name)
            st.session_state.business_name = business_name
        
        # Save User Message to DB
        add_message(st.session_state.supabase, st.session_state.current_conversation_id, "user", prompt)
        st.session_state.messages.append(HumanMessage(content=prompt))
        
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            with st.status("Thinking...", expanded=True) as status:
                # Run Graph
                config = {"configurable": {"thread_id": str(st.session_state.current_conversation_id)}}
                inputs = {
                    "messages": st.session_state.messages, 
                    "user_id": st.session_state.user.id,
                    "business_name": st.session_state.get("business_name", "N/A")
                }
                
                async for chunk in graph.astream(inputs, config):
                    if "agent" in chunk:
                        msg = chunk["agent"]["messages"][-1]
                        content = msg.content
                        
                        # Handle content if it's a list (content blocks)
                        if isinstance(content, list):
                            full_response = "".join([c.get("text", "") if isinstance(c, dict) else str(c) for c in content])
                        else:
                            full_response = str(content)
                            
                        message_placeholder.markdown(full_response)
                
                status.update(label="Complete!", state="complete", expanded=False)
            
            # Check for tool results (like logo URL)
            extras = {}
            # In our case, the logo agent returns the URL in the text.
            # We can extract it with regex if we want to show it nicely.
            logo_match = re.search(r"available at: (https://\S+)", full_response)
            if logo_match:
                extras["logo_url"] = logo_match.group(1)
                st.image(extras["logo_url"], width=300)

            # Save Assistant Message to DB
            add_message(st.session_state.supabase, st.session_state.current_conversation_id, "assistant", full_response, extras)
            st.session_state.messages.append(AIMessage(content=full_response, response_metadata={"extras": extras}))

# Routing
if st.session_state.current_page == "Home":
    show_home()
elif st.session_state.current_page == "Login":
    show_login()
elif st.session_state.current_page == "Chatbot":
    asyncio.run(show_chatbot())
