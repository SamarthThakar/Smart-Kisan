"""RAG Engine — ChromaDB + Google Gemini 1.5 Flash"""
import os
from typing import List, Optional, Dict, Any
from pathlib import Path

from app.config import settings

_chroma_client = None
_collection = None
_gemini_model = None

SYSTEM_PROMPT = """You are Kisan Mitra (किसान मित्र), a knowledgeable and friendly agricultural expert assistant for Indian farmers.

IMPORTANT RULES:
1. Answer ONLY agriculture-related questions (crops, diseases, farming practices, irrigation, fertilizers, pesticides, government schemes, market prices, weather interpretation).
2. If asked about non-agricultural topics, politely redirect: "I can only help with farming and agriculture questions. Please ask me about your crops, soil, weather, or government schemes."
3. Use simple, practical language that farmers can understand.
4. When relevant context is provided, base your answer primarily on that context.
5. For government scheme details, always remind the farmer to verify at the official website.
6. Do NOT invent statistics, prices, or scheme details.
7. If you're unsure, say so and recommend consulting a local Krishi Vigyan Kendra (KVK) or agricultural extension officer.
8. Respond in the SAME LANGUAGE as the question (English/Hindi/Marathi).
9. Keep responses concise and actionable — farmers need practical advice.
10. End serious disease or pest alerts with: "For urgent cases, contact your nearest KVK immediately."

You have access to agricultural knowledge from ICAR guidelines, government scheme information, and farming best practices."""


def _initialize_gemini():
    """Initialize Gemini model"""
    global _gemini_model
    if _gemini_model is not None:
        return _gemini_model
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        _gemini_model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_PROMPT
        )
        print("✅ Gemini model initialized")
        return _gemini_model
    except Exception as e:
        print(f"❌ Failed to initialize Gemini: {e}")
        return None


def _initialize_chroma():
    """Initialize ChromaDB client and collection"""
    global _chroma_client, _collection
    
    if _collection is not None:
        return _collection
    
    try:
        import chromadb
        chroma_path = Path(settings.CHROMA_DB_PATH)
        chroma_path.mkdir(parents=True, exist_ok=True)
        
        _chroma_client = chromadb.PersistentClient(path=str(chroma_path))
        _collection = _chroma_client.get_or_create_collection(
            name="agricultural_knowledge",
            metadata={"hnsw:space": "cosine"}
        )
        print(f"✅ ChromaDB initialized. Documents: {_collection.count()}")
        return _collection
    except Exception as e:
        print(f"❌ Failed to initialize ChromaDB: {e}")
        return None


async def get_rag_response(
    query: str,
    language: str = "en",
    history: List = None
) -> Dict[str, Any]:
    """
    Main RAG function: retrieve relevant context + generate Gemini response.
    """
    model = _initialize_gemini()
    collection = _initialize_chroma()
    
    if model is None:
        return {
            "response": "AI assistant is temporarily unavailable. Please try again later.",
            "sources": []
        }
    
    # Retrieve relevant context from ChromaDB
    context = ""
    sources = []
    
    if collection and collection.count() > 0:
        try:
            results = collection.query(
                query_texts=[query],
                n_results=min(3, collection.count()),
                include=["documents", "metadatas", "distances"]
            )
            
            if results["documents"] and results["documents"][0]:
                context_parts = []
                for i, (doc, meta, dist) in enumerate(zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )):
                    # Only use highly relevant results
                    if dist < 0.7:
                        context_parts.append(f"[Source {i+1}]: {doc}")
                        if meta.get("source"):
                            sources.append(meta["source"])
                
                if context_parts:
                    context = "\n\n".join(context_parts)
        except Exception as e:
            print(f"ChromaDB query failed: {e}")
    
    # Build prompt
    language_instruction = {
        "en": "Respond in English.",
        "hi": "हिंदी में जवाब दें।",
        "mr": "मराठीत उत्तर द्या."
    }.get(language, "Respond in English.")
    
    if context:
        prompt = f"""Relevant agricultural knowledge:
{context}

Based on the above information, answer this farmer's question:
{query}

{language_instruction}"""
    else:
        prompt = f"""{query}

{language_instruction}"""
    
    # Build conversation history for Gemini
    chat_history = []
    if history:
        for msg in history[-4:]:  # Last 2 exchanges
            role = "user" if msg.role == "user" else "model"
            chat_history.append({"role": role, "parts": [msg.content]})
    
    try:
        if chat_history:
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(prompt)
        else:
            response = model.generate_content(prompt)
        
        return {
            "response": response.text,
            "sources": list(set(sources))  # Deduplicate sources
        }
    except Exception as e:
        print(f"Gemini API error: {e}")
        return {
            "response": (
                "I'm having trouble responding right now. Please try again in a moment. "
                "For urgent farming advice, contact your local Krishi Vigyan Kendra (KVK)."
            ),
            "sources": []
        }
