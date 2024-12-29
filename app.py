from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pytube import YouTube
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DownloadRequest(BaseModel):
    url: str

@app.post("/download")
async def download_audio(request: DownloadRequest):
    try:
        # Create YouTube object
        yt = YouTube(request.url)
        
        # Get audio stream
        audio = yt.streams.filter(only_audio=True).first()
        
        # Download
        out_file = audio.download()
        
        # Rename to mp3
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        
        return {
            "title": yt.title,
            "duration": yt.length,
            "filename": os.path.basename(new_file)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def read_root():
    return {"status": "alive"}