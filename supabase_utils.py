import os
from datetime import datetime
from typing import List, Dict, Optional
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

def get_supabase_client(admin: bool = False):
    """Creates a fresh Supabase client instance. Use admin=True for system operations."""
    key = SUPABASE_SERVICE_KEY if admin and SUPABASE_SERVICE_KEY else SUPABASE_KEY
    return create_client(SUPABASE_URL, key)

# --- AUTHENTICATION ---

def sign_up(supabase: Client, email: str, password: str):
    """Signs up a new user using email and password."""
    return supabase.auth.sign_up({"email": email, "password": password})

def sign_in(supabase: Client, email: str, password: str):
    """Signs in an existing user."""
    return supabase.auth.sign_in_with_password({"email": email, "password": password})

def sign_out(supabase: Client):
    """Signs out the current user."""
    return supabase.auth.sign_out()

# --- DATABASE OPERATIONS ---

def create_conversation(supabase: Client, user_id: str, title: str, business_name: str) -> str:
    """Creates a new conversation thread."""
    data = {
        "user_id": user_id,
        "title": title,
        "business_name": business_name,
        "created_at": datetime.now().isoformat()
    }
    result = supabase.table("conversations").insert(data).execute()
    return result.data[0]["id"]

def get_user_conversations(supabase: Client, user_id: str) -> List[Dict]:
    """Retrieves all conversation threads for the specifically logged-in user."""
    # We filter by user_id explicitly. 
    # If RLS(row-level security) is enabled, Supabase will also double-check this against the session token.
    try:
        result = supabase.table("conversations")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("created_at", desc=True)\
            .execute()
        return result.data
    except Exception as e:
        print(f"Error fetching conversations: {e}")
        return []

def add_message(supabase: Client, conversation_id: str, role: str, content: str, extras: Optional[Dict] = None):
    """Adds a message to a conversation."""
    data = {
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
        "extras": extras or {},
        "created_at": datetime.now().isoformat()
    }
    return supabase.table("messages").insert(data).execute()

def get_conversation_messages(supabase: Client, conversation_id: str) -> List[Dict]:
    """Retrieves all messages in a conversation."""
    result = supabase.table("messages")\
        .select("*")\
        .eq("conversation_id", conversation_id)\
        .order("created_at", desc=False)\
        .execute()
    return result.data

# --- STORAGE OPERATIONS ---

def upload_logo(supabase: Client, user_id: str, business_name: str, image_bytes: bytes) -> str:
    """Uploads a generated logo to Supabase Storage and returns the public URL."""
    filename = f"{user_id}/{business_name.replace(' ', '_')}_{int(datetime.now().timestamp())}.png"
    
    # Upload to 'logos' bucket
    supabase.storage.from_("logos").upload(
        path=filename,
        file=image_bytes,
        file_options={"content-type": "image/png"}
    )
    
    # Get public URL
    return supabase.storage.from_("logos").get_public_url(filename)
