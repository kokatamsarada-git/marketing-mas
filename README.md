# Marketing Agency AI Assistant

A sophisticated multi-agent AI system powered by AWS Bedrock and LangGraph that provides comprehensive marketing automation and strategy services.

## 🎯 Overview

This project implements an intelligent marketing agency using multiple specialized AI agents. Each agent is designed to handle specific marketing tasks, from strategy development to content creation, leveraging AWS Bedrock's Anthropic models for high-quality AI responses.

## ✨ Features

- **Multi-Agent Architecture**: Specialized agents for different marketing functions
- **Real-time Streaming**: Stream responses in real-time via Streamlit UI or CLI
- **AWS Bedrock Integration**: Powered by Claude models for superior AI capabilities
- **Conversation Memory**: Maintains conversation history for context-aware responses
- **Tool-Based System**: Agents equipped with specialized tools for specific marketing tasks
- **Flexible UI**: Both web-based (Streamlit) and command-line interfaces

## 🏗️ Architecture

The system uses **LangGraph** to orchestrate an agentic workflow:

```
User Input → Agent Node → Tool Evaluation → Tool Execution → Response
                ↑_____________↓________________↓______________|
```

- **Agent Node**: Main reasoning loop using Claude Sonnet 4.6
- **Tool Node**: Executes specialized marketing tools
- **Conditional Routing**: Dynamically decides whether to call tools or respond directly

## 🤖 Available Agents

The system includes the following specialized agents:

| Agent | Purpose |
|-------|---------|
| **Strategy Agent** | Create comprehensive marketing strategies |
| **Ad Copy Agent** | Generate compelling advertisement copy |
| **Email Campaign Agent** | Design email marketing campaigns |
| **Social Media Agent** | Create social media content and strategies |
| **SEO Agent** | Develop SEO strategies and keyword optimization |
| **Logo Agent** | Generate logo design concepts and briefs |
| **Tag Line Agent** | Create catchy business taglines |
| **Domain Agent** | Handle domain-related recommendations |

## 📋 Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- AWS credentials configured
- Internet connection

## 🚀 Getting Started

### Installation

1. **Clone the repository** (or navigate to the project directory)
   ```bash
   cd "Marketing Agent"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - **Windows PowerShell**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows CMD**:
     ```cmd
     venv\Scripts\activate.bat
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure AWS Credentials**
   
   Create a `.env` file in the project root:
   ```env
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_DEFAULT_REGION=us-east-1
   ```

   Or configure via AWS CLI:
   ```bash
   aws configure
   ```

## 💻 Usage

### Web Interface (Streamlit)

Run the interactive web-based interface:

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

**Features:**
- Chat interface with streaming responses
- Logo image display support
- Conversation history
- Real-time token streaming

### Command Line Interface (CLI)

Run the CLI version for terminal-based interaction:

```bash
python cli.py
```

**Features:**
- Simple text-based interaction
- Type 'quit' or 'exit' to end the session
- Conversation history maintained during session

**Example:**
```
You: Create a marketing strategy for a fitness app startup
Agent: [Comprehensive strategy response...]

You: What would be a good tagline?
Agent: [Tagline suggestions...]
```

## 📦 Project Structure

```
Marketing Agent/
├── app.py                 # Streamlit web interface
├── cli.py                 # Command-line interface
├── requirements.txt       # Python dependencies
│
├── agents/                # Specialized marketing agents
│   ├── __init__.py       # Agent exports
│   ├── strategy_agent.py
│   ├── ad_copy_agent.py
│   ├── email_campaign_agent.py
│   ├── social_media_agent.py
│   ├── seo_agent.py
│   ├── logo_agent.py
│   ├── tag_line_agent.py
│   └── domain_agent.py
│
└── graph/                 # LangGraph workflow
    ├── __init__.py
    ├── graph.py          # Main agent graph definition
    ├── prompt.py         # System prompts
    └── state.py          # State management
```

## 🔧 Configuration

### Environment Variables

- `AWS_ACCESS_KEY_ID`: AWS access key for Bedrock API
- `AWS_SECRET_ACCESS_KEY`: AWS secret key for Bedrock API
- `AWS_DEFAULT_REGION`: AWS region (default: us-east-1)

### Models Used

- **Agent Reasoning**: `claude-sonnet-4-6` (advanced reasoning)
- **Tool Execution**: `claude-haiku-4-5-20251001-v1:0` (fast, efficient)

## 🎨 Example Workflows

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
