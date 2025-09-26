from fastapi import FastAPI
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pytz
from typing import List
from fastapi import UploadFile
from .supabaseClient import supabase
from datetime import datetime
from .flow import run_ai_agent

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API is running"}


@app.get("/fetch_podcast")
async def fetch_podcast():
    podcasts = supabase.table("Podcasts").select("*, timezone, topicId(topic), city(cityName), speaker1(speakerName), speaker2(speakerName), language(languageName)").order("createdAt",desc=True).execute().data

    jakarta_tz = pytz.timezone("Asia/Jakarta")

    for item in podcasts:
        # Parse the original UTC timestamp
        dt_utc = datetime.fromisoformat(item['createdAt'])

        # Convert to Jakarta time
        dt_local = dt_utc.astimezone(jakarta_tz)

        # Format to desired style
        item['createdAt'] = dt_local.strftime("%d %b %Y %I:%M %p")

    return {"podcasts": podcasts}

@app.post("/generate_podcast/")
async def generate_podcast(
    description: str = Form(...),
    language: str = Form(...),
    duration: int = Form(...),
    style: str = Form(...),
    format: str = Form(...),
    bgm: bool = Form(...),
    speakers: List[str] = Form(...),
    files: List[UploadFile] = File(None)
):
    result_url = await run_ai_agent(
        description, language, 
        duration, style, 
        format, bgm, 
        speakers, files
    )

    return {"public_url": result_url}



