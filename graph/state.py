
from langgraph.graph import MessagesState


class AgentState(MessagesState):
    """State class for agents to carry the coversation history and other relevant information."""
    user_id: str
    conversation_id: str
    business_name: str
