from fastapi import FastAPI
from yt_dlp import YoutubeDL
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request model
class DownloadRequest(BaseModel):
    url: str

@app.post("/download")
async def download_audio(request: DownloadRequest):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': '%(title)s.%(ext)s',  # Save with video title as filename
        'cookiesfrombrowser': ('chrome',),  # Use cookies from Chrome browser
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(request.url, download=True)
            return {
                "title": info.get('title'),
                "duration": info.get('duration'),
                "filename": f"{info.get('title')}.mp3"
            }
        except Exception as e:
            return {"error": str(e)}

@app.get("/")
async def read_root():
    return {"status": "alive"}