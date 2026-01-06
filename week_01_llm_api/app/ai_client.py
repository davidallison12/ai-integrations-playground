import json
from enum import Enum
from openai import OpenAI
from pydantic import BaseModel # Used for request body

# ==========================
#  OPEN AI CLIENT
# ==========================
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
    response = client.response.create(
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

    print(response.model_dump())
    response_raw_text = response.output[0].content[0].text
    parsed_response = json.loads(response_raw_text)

    return parsed_response 



