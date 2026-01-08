import json
import os
from dotenv import load_dotenv
from enum import Enum
from openai import OpenAI
from pydantic import BaseModel # Used for request body

# ==========================
#  OPEN AI CLIENT
# ==========================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set")


client = OpenAI()



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


# ==============================
# SENTIMENT SUMMARY W/ OPEN AI
# ==============================
def get_sentiment_summary(record_id, message):
    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {
                "role":"system", 
                "content":(
                    "You are an analysis service. "
                    "Given the input text, return ONLY a valid JSON object with the following structure:\n\n"
                    "{\n"
                    '  "summary": string,                 \n'
                    '  "sentiment": "positive" | "neutral" | "negative",\n'
                    '  "confidence": number               \n'
                    "}\n\n"
                    "Rules:\n"
                    "- Respond with JSON only. No additional text.\n"
                    "- Do not include explanations or comments.\n"
                    "- Ensure the JSON is syntactically valid.\n"
                    '- If you are unsure about the sentiment, choose "neutral" and lower the confidence score.'
                )
            },
            {
                "role": "user", 
                "content": f"record_id:{record_id}, message: {message}"
            }
        ]
    )

    # print(response.model_dump())
    parsed_response = extract_json_from_response(response)

    return parsed_response 


def extract_json_from_response(response):
    """
    Takes the output text(JSON) response returned as 'ResponseReasoningItem'
    object and extracts it to python object
    """
    for item in response.output:
        if item.type == "message":
            for content in item.content:
                if content.type == "output_text":
                    return json.loads(content.text)
    raise ValueError("Appripriate output not found")



if __name__ == "__main__":
    result = get_sentiment_summary(
        record_id=123,
        message="The service was fast and the support team was very helpful."
    )
    print(result)

