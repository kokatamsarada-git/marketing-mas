# 🚀 Brand Boost AI: Your Personal Marketing Agency

A sophisticated multi-agent AI system powered by **AWS Bedrock** and **LangGraph** that provides comprehensive marketing automation, branding, and strategy services.

## 🎯 Overview

BrandBoost AI is an intelligent marketing agency orchestrated by multiple specialized AI agents. From developing comprehensive marketing strategies to generating professional logos and catchy taglines, the system leverages AWS Bedrock's Anthropic Claude 3.5 Sonnet models to deliver expert-level marketing collateral.

## ✨ Features

- **Premium UI/UX**: Professional Streamlit interface with a modern look and feel.
- **Multi-Agent Intelligence**: Specialized agents for strategy, SEO, ads, social media, and more.
- **Visual Branding**: Integrated **Amazon Titan Image Generator** for professional logo creation.
- **Organized Storage**: All generated logos are automatically sanitized and stored in a dedicated `generated_logos/` directory.
- **Real-time Streaming**: Instant feedback with token-level streaming and tool execution status boxes.
- **Interactive Campaign Management**: Sidebar controls to reset campaigns and view quick suggestions.
- **One-Click Downloads**: Direct download buttons for generated visual assets.

## 🏗️ Architecture

The system uses **LangGraph** to manage a dynamic, stateful workflow:

```
User Input → BrandBoost Agent → Tool Evaluation → Tool Execution → Response
                  ↑_________________↓___________________↓__________________|
```

- **Reasoning Engine**: Claude 3.5 Sonnet (Advanced Reasoning)
- **Tool Executor**: Claude 3 Haiku (Fast & Efficient)
- **Image Engine**: Amazon Titan Image Generator V2

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

Launch the modern branding dashboard:

```bash
streamlit run app.py
```

**Features:**
- **Status Indicators**: Real-time `st.status` boxes showing agent activity.
- **Logo Gallery**: Expandable visual branding sections with path confirmation.
- **Asset Download**: One-click download buttons for generated PNGs.
- **Campaign Reset**: Quick-start button in the sidebar to begin fresh.

### Command Line Interface (CLI)

For lightweight text-based interaction:

```bash
python cli.py
```

## 📦 Project Structure

```
Marketing Agent/
├── app.py                 # Premium Streamlit UI
├── cli.py                 # Terminal-based interface
├── requirements.txt       # Core dependencies
├── generated_logos/       # Auto-created repository for visual assets
│
├── agents/                # Intelligent Agent Definitions
│   ├── strategy_agent.py  # Marketing planning
│   ├── logo_agent.py      # Titan Image integration
│   ├── seo_agent.py       # SEO & Keyword research
│   └── ...                # Other specialized agents
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
