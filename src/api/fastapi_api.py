"""
The backend: a small FastAPI service that improves input.

Use any one option to run:
    fastapi dev src/api/fastapi_api.py
    python -m fastapi dev src/api/fastapi_api.py
    uv run fastapi dev src/api/fastapi_api.py

Then the Streamlit app (streamlit_app.py) will call this service for every request.
"""

import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
app = FastAPI()


# Welcome message 
@app.get("/")
def home():
    return {"message": "Welcome To Data Improvement API"}


# What the caller must SEND us
class Input(BaseModel):
    request: str = Field(min_length=10, max_length=50)

    @field_validator("request")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Input text must not be blank.")
        return value


# What Gemini gives back, and what we SEND to the caller.
class Output(BaseModel):
    response: str


@app.post("/improve")
def improve(input: Input) -> Output:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="GOOGLE_API_KEY is not configured.")

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=(
                "Improve input information.\n"
                "Improved input must be less than 100 words .\n"
                f"Input: {input.request}"
            ),
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=Output,
            ),
        )
        if response.parsed is None:
            raise HTTPException(status_code=502, detail="The model returned no structured result.")
        return response.parsed
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail="The improvement service is unavailable.") from exc
