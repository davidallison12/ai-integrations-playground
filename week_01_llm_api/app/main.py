from enum import Enum
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel # Used for request body
from typing import Literal
import os

# ==========================
# LOAD ENVIRONEMENT VARIABLE
# ==========================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set")


app = FastAPI()



# ==========================
# API ENDPOINTS
# ==========================

# Health Endpoint 
@app.get("/health")
async def health():
    return {"status": "ok"}


# ===================================
# POST /analyze
# input: text
# output: summary + sentiment (w/ request Id, confidence + fallback used boolean)
# constraints:
# - structured JSON
# - deterministic
# ===================================
class SentimentTypes(str, Enum):
    NEGATIVE = "negative"
    POSITIVE = "positive"
    NEUTRAL = "neutral"

class SentimentSummary(BaseModel):
    request_id: str
    summary: str
    sentiment: str
    confidence: float
    fallback_used: bool

# Note: Can use Literal[] in order to create specific approved values or use Enum
class Summary(BaseModel):
    summary: str | None = None
    sentiment: Literal["positive", "negative"] | None = None  # positive, negative, neutral


@app.post("/analyze/")
async def create_summary(summary: Summary): # Define request body template here
    # Will add record_id (Can save to db/random number for now)



    return summary
