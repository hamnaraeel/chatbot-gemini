from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Prompt(BaseModel):
    text: str

# Configure the Gemini API
GOOGLE_API_KEY = "AIzaSyAnOH3LNGA8xo43zfTkEsppoF55OMOB7N0"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

@app.post("/chat/")
async def chat_with_gemini(prompt: Prompt):
    try:
        response = model.generate_content(prompt.text)
        return {"response": response.text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/")
async def chat_with_gemini_get(query: str = Query(..., description="The query text to send to Gemini")):
    try:
        response = model.generate_content(query)
        return {"response": response.text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
