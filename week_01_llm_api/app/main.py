from fastapi import FastAPI
from pydantic import BaseModel # Used for request body
from typing import Literal

app = FastAPI()

# Health Endpoint 
@app.get("/health")
async def health():
    return {"status": "ok"}


# POST /analyze
# input: text
# output: summary + sentiment (w/ request Id, confidence + fallback used boolean)
# constraints:
# - structured JSON
# - deterministic

# Note: Can use Literal[] in order to create specific approved values or use Enum
class Summary(BaseModel):
    summary: str | None = None
    sentiment: Literal["positive", "negative"] | None = None  # positive, negative, neutral


@app.post("/analyze/")
async def create_summary(summary: Summary): # Define request body template here
    return summary