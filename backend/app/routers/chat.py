"""AI Chat Router — Gemini 1.5 Flash + RAG with ChromaDB"""
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional
import os

from app.database import get_db
from app.models import ChatHistory, User
from app.core.security import get_current_user
from app.config import settings
from app.ml.rag_engine import get_rag_response

router = APIRouter()


class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User's message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    language: str = Field(default="en", pattern="^(en|hi|mr)$")


@router.post("")
async def chat(
    chat_input: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    AI Farmer Assistant using Gemini 1.5 Flash + RAG.
    Answers agriculture-related questions in English, Hindi, or Marathi.
    """
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "REPLACE_WITH_YOUR_GEMINI_API_KEY":
        # Fallback response when Gemini API not configured
        return _get_fallback_response(chat_input.message, chat_input.language)

    # Create or continue session
    session_id = chat_input.session_id or str(uuid.uuid4())

    # Get recent conversation history for context
    history = (
        db.query(ChatHistory)
        .filter(
            ChatHistory.user_id == current_user.id,
            ChatHistory.session_id == session_id
        )
        .order_by(ChatHistory.created_at.desc())
        .limit(6)  # Last 3 exchanges (user + assistant = 6 messages)
        .all()
    )
    conversation_history = list(reversed(history))

    # Get AI response via RAG
    response_data = await get_rag_response(
        query=chat_input.message,
        language=chat_input.language,
        history=conversation_history
    )

    # Save user message
    user_msg = ChatHistory(
        user_id=current_user.id,
        session_id=session_id,
        role="user",
        content=chat_input.message,
        language=chat_input.language,
    )
    db.add(user_msg)

    # Save assistant response
    assistant_msg = ChatHistory(
        user_id=current_user.id,
        session_id=session_id,
        role="assistant",
        content=response_data["response"],
        language=chat_input.language,
        sources_used=response_data.get("sources", [])
    )
    db.add(assistant_msg)
    db.commit()

    return {
        "response": response_data["response"],
        "session_id": session_id,
        "sources": response_data.get("sources", []),
        "language": chat_input.language,
        "message_id": assistant_msg.id
    }


@router.get("/history")
async def get_chat_history(
    session_id: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chat history for current user"""
    query = db.query(ChatHistory).filter(ChatHistory.user_id == current_user.id)
    if session_id:
        query = query.filter(ChatHistory.session_id == session_id)
    
    messages = query.order_by(ChatHistory.created_at.asc()).limit(limit).all()
    
    return {
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "language": m.language,
                "sources": m.sources_used,
                "created_at": m.created_at.isoformat()
            }
            for m in messages
        ],
        "session_id": session_id
    }


def _get_fallback_response(message: str, language: str) -> dict:
    """Friendly fallback when Gemini API is not configured"""
    responses = {
        "en": (
            "🌾 Hello! I'm Kisan Mitra, your agricultural assistant. "
            "To enable the full AI assistant, please configure your Gemini API key in the .env file. "
            "Get a free key at: https://aistudio.google.com/app/apikey\n\n"
            "In the meantime, you can use the Disease Detection, Crop Recommendation, "
            "Weather Advisory, and Market Price features which work without the AI assistant."
        ),
        "hi": (
            "🌾 नमस्ते! मैं किसान मित्र हूं। AI सहायक को सक्रिय करने के लिए, "
            "कृपया .env फ़ाइल में अपनी Gemini API key जोड़ें। "
            "मुफ़्त key यहाँ से लें: https://aistudio.google.com/app/apikey"
        ),
        "mr": (
            "🌾 नमस्कार! मी किसान मित्र आहे। AI सहाय्यक सक्रिय करण्यासाठी "
            ".env फाइलमध्ये Gemini API key जोडा।"
        )
    }
    return {
        "response": responses.get(language, responses["en"]),
        "session_id": str(uuid.uuid4()),
        "sources": [],
        "language": language,
        "is_demo_mode": True,
        "message_id": str(uuid.uuid4())
    }
