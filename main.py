from fastapi import FastAPI, UploadFile, File
import shutil
import os
from .ai_engine import get_viral_segments
from .video_processor import process_video

app = FastAPI()

# Ensure directories exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

@app.get("/")
async def read_root():
    return {"status": "Online", "message": "AttentionX is active. Use /docs to test."}

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        from moviepy.editor import VideoFileClip
        temp_clip = VideoFileClip(file_path)
        safe_duration = min(10, temp_clip.duration) # Take 10s or the whole video if shorter
        temp_clip.close()

        print(f"[EMERGENCY] Creating a {safe_duration}s demo clip...")
        viral_info = [{"start": 0, "end": safe_duration, "text": "AttentionX AI"}]
        
        print("[STEP 3] Calling MoviePy Processor...")
        clips = process_video(file_path, viral_info) 
        
        return {
            "status": "Success", 
            "message": "Vertical Demo Created!",
            "clips": clips
        }
    except Exception as e:
        print(f"[CRITICAL ERROR] {str(e)}")
        return {"status": "Error", "message": str(e)}