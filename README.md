# 🚀 Brand Boost AI: Your Personal Marketing Agency

A sophisticated multi-agent AI system powered by **AWS Bedrock** and **LangGraph** that provides comprehensive marketing automation, branding, and strategy services.

## 🎯 Overview

BrandBoost AI is an intelligent marketing agency orchestrated by multiple specialized AI agents. From developing comprehensive marketing strategies to generating professional logos and catchy taglines, the system leverages AWS Bedrock's Anthropic Claude 3.5 Sonnet models to deliver expert-level marketing collateral.

## ✨ Features

- **Multi-User SaaS Architecture**: Secure user authentication and session isolation via **Supabase Auth**.
- **Conversation Persistence**: Complete chat history stored in **Supabase Database**, allowing users to resume previous campaigns across devices.
- **Cloud Asset Storage**: Generated logos are uploaded to **Supabase Storage** and linked to user profiles for permanent access.
- **Competitor Intelligence**: New agent for deep-dive competitor analysis from any URL.
- **Premium Multi-Page UI**: Dedicated Home, Auth, and Chatbot pages with a modern, responsive design and persistence sidebar.

## 🏗️ Architecture

The system uses **LangGraph** for workflow orchestration and **Supabase** for the backend:

- **Frontend**: Streamlit (Multipage)
- **Backend**: Supabase (Auth, Database, Storage)
- **AI Engine**: AWS Bedrock (Claude 3.5 Sonnet, Claude 3 Haiku)
- **Image Engine**: Amazon Titan Image Generator V2

## 📋 Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- Supabase Project (URL and API Key)
- AWS credentials configured

## 🚀 Getting Started

### Installation

1. **Clone the repository** (or navigate to the project directory)
   ```bash
   cd "Marketing Agent"
   ```

2. **Set up Environment Variables**
   
   Create a `.env` file in the project root:
   ```env
   # AWS Configuration
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_DEFAULT_REGION=us-east-1

   # Supabase Configuration
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your-anon-key
   SUPABASE_SERVICE_KEY=your-service-role-key
   ```

3. **Initialize Supabase Schema**
   - Run the SQL commands from `schema.sql` in your Supabase SQL Editor.
   - Create a storage bucket named `logos` in your Supabase dashboard.
   - **Important**: Disable "Email Confirmation" in Supabase Auth settings to allow immediate logins.

4. **Install and Run**
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```

## 💻 Usage

### Web Interface (Streamlit)

Launch the modern branding dashboard:

```bash
streamlit run app.py
```

**Features:**
- **Status Indicators**: Real-time `st.status` boxes showing agent activity.
- **Logo Gallery**: Cloud-hosted visual branding sections.
- **Asset Download**: One-click download buttons for generated PNGs from Supabase Storage.
- **Campaign History**: Persistence sidebar to view previous chat sessions.
- **Campaign Reset**: Quick-start button in the sidebar to begin fresh.

## 📦 Project Structure

```
Marketing Agent/
├── app.py                 # Premium Multi-page Streamlit UI
├── supabase_utils.py      # Supabase Auth, DB, and Storage logic
├── schema.sql             # SQL definitions for conversations & RLS
├── requirements.txt       # Core dependencies
│
├── agents/                # Intelligent Agent Definitions
│   ├── competitor_agent.py # Competitive analysis agent [NEW]
│   ├── strategy_agent.py   # Marketing planning
│   ├── logo_agent.py       # Bedrock Titan integration
│   └── ...                 # Other specialized agents
│
└── graph/                 # LangGraph Workflow Orchestration
    ├── graph.py          # State machine definition
    ├── prompt.py         # Advanced system instructions
    └── state.py          # Session state management
```

## 🔧 Configuration

### Environment Variables

- `AWS_ACCESS_KEY_ID`: AWS access key for Bedrock API
- `AWS_SECRET_ACCESS_KEY`: AWS secret key for Bedrock API
- `AWS_DEFAULT_REGION`: AWS region (default: us-east-1)

### Models Used

- **Primary Model**: `Claude 3.5 Sonnet` (Advanced reasoning & orchestration)
- **Image Generation**: `Amazon Titan Image Generator V2`

| Agent | Purpose |
|-------|---------|
| **Competitor Agent** | Analyze rivals and generate deep competitive reports |
| **Strategy Agent** | Create comprehensive marketing strategies |
| **Ad Copy Agent** | Generate compelling advertisement copy |
| **Email Campaign Agent** | Design email marketing campaigns |
| **Social Media Agent** | Create social media content and strategies |
| **SEO Agent** | Develop SEO strategies and keyword optimization |
| **Logo Agent** | Generate logo design concepts and visual branding |
| **Tag Line Agent** | Create catchy business taglines |
| **Domain Agent** | Handle domain-related recommendations |

### Marketing Strategy Creation
```
User: "I'm starting a sustainable fashion brand. Help me create a marketing strategy."
Agent: [Uses Strategy Agent to analyze target market, channels, messaging, etc.]
```

### Multi-Agent Coordination
```
User: "Create ad copy, social media post, and email campaign for my new product launch"
Agent: [Coordinates multiple agents to deliver comprehensive campaign materials]
```

## 🛠️ Dependencies

- `langgraph>=0.2` - Workflow orchestration
- `langchain-aws>=0.2` - AWS Bedrock integration
- `langchain-core>=0.3` - Core LLM abstraction
- `python-dotenv>=1.0` - Environment configuration
- `boto3>=1.34` - AWS SDK
- `streamlit>=1.35` - Web interface
- `supabase>=2.4` - Backend as a Service
- `streamlit-option-menu` - Navigation component

## 📝 API Reference

### Core Functions

#### `graph.ainvoke(input_dict)`
Async invocation of the agent graph.

```python
result = await graph.ainvoke({
    "messages": [HumanMessage(content="Your query")]
})
```

#### `graph.astream_events(input_dict)`
Async streaming of events for real-time token output.

```python
async for event in graph.astream_events({"messages": messages}, version="v2"):
    # Process streaming events
```

## 🔒 Security Considerations

- Never commit `.env` files with credentials
- Use IAM roles when possible instead of hardcoded credentials
- Rotate AWS credentials regularly
- Use least privilege IAM policies for Bedrock access

## 📖 Further Reading

- [AWS Bedrock Documentation](https://aws.amazon.com/bedrock/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 📄 License

This project is part of the Python exercises collection.

## 🤝 Support

For issues or questions:
1. Check that AWS credentials are properly configured
2. Verify Bedrock access is enabled in your AWS account
3. Ensure all dependencies are installed: `pip install -r requirements.txt`
4. Check that you're in the correct Python virtual environment

---

**Built with:** Python, LangGraph, AWS Bedrock, Streamlit, LangChain
