"""FastAPI service for Assignment 26."""

import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from main import groq_chat

app = FastAPI(
    title="Assignment 26 - Groq Chatbot API",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    query: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    answer: str
    model: str


@app.get("/")
def home():
    return {"message": "Groq Chatbot API is running", "docs": "/docs"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        answer = groq_chat(request.query)
        return ChatResponse(
            answer=answer,
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Groq request failed: {type(exc).__name__}: {exc}",
        )
