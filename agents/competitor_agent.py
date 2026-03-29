from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

_llm = ChatBedrock(model="global.anthropic.claude-haiku-4-5-20251001-v1:0")

@tool
def analyze_competitor(competitor_url: str, business_name: str = "N/A") -> str:
    """Perform a competitive analysis for a given competitor URL.
    Use this tool when the user provides a competitor's website or asks for 
    competitive intelligence, market positioning, or comparison with rivals."""
    
    # In a real-world scenario, we would use a web-scraping tool or Search API here.
    # Since we are focusing on the agent orchestration, we'll prompt the LLM to 
    # analyze based on its internal knowledge of the URL (if famous) or 
    # provide a structured framework for the user to fill in if the URL is new.
    
    prompt = (
        f"Perform a comprehensive competitive analysis for the following competitor: {competitor_url}\n"
        f"Our Business: {business_name}\n\n"
        f"Please provide the analysis in the following format:\n"
        f"1. **Market Positioning**: How do they position themselves?\n"
        f"2. **Core Offerings**: Key products or services.\n"
        f"3. **Strengths**: What are they doing well?\n"
        f"4. **Weaknesses**: Where is there an opportunity for us?\n"
        f"5. **Marketing Strategy**: Observations on their digital presence (ads, social, content).\n"
        f"6. **Strategic Recommendation**: How should '{business_name}' respond or differentiate?\n\n"
        f"Provide a professional, detailed report."
    )
    
    response = _llm.invoke([HumanMessage(content=prompt)])
    
    return (
        f"### 🛡️ Competitor Analysis Report: {competitor_url}\n\n"
        f"{response.content}\n\n"
        f"--- \n"
        f"*Note: This analysis is based on available data for the provided URL. "
        f"If you'd like more specific insights, feel free to provide more details about their pricing or recent campaigns!*"
    )
