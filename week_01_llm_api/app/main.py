from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
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

# ==========================
# API ENDPOINTS
# ==========================
app = FastAPI()
client = OpenAI()

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

# Note: Can use Literal[] in order to create specific approved values or use Enum
class Summary(BaseModel):
    summary: str | None = None
    sentiment: Literal["positive", "negative"] | None = None  # positive, negative, neutral


@app.post("/analyze/")
async def create_summary(summary: Summary): # Define request body template here
    return summary



# You must pay to use any of the models / Not ideal for those just looking to learn in a cheap manner
# Pay attention to usage in order to manage spend 


# ==========================
# TEST EXAMPLE USING OPEN AI
# ==========================
# response = client.responses.create(
#     model="gpt-5-nano", # This looks to be the cheapest model you can use. 
#     input="Write a one-sentence bedtime story about a unicorn."
# )

# print(response.output_text) 
# Response: Under the silver moon, a gentle unicorn curled up on a bed of clover and drifted into a dream where the stars sang lullabies.