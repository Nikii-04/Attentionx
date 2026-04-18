import google.generativeai as genai
import whisper
import re

# Initialize Gemini
# Replace YOUR_GEMINI_API_KEY with the key from Google AI Studio
genai.configure(api_key="AIzaSyAEl1DJkzpCAgGedP2XzYVbN3WUjPXiII0") 
model = genai.GenerativeModel('gemini-1.5-flash')

def get_viral_segments(video_path):
    # 1. Transcribe audio using Whisper to get text with timestamps
    print("Transcribing video...")
    whisper_model = whisper.load_model("base")
    result = whisper_model.transcribe(video_path)
    full_text = result['text']
    
    # 2. Ask Gemini 1.5 Flash to identify high-impact moments
    print("Analyzing for viral nuggets...")
    prompt = (
        f"You are a social media expert. Analyze this transcript and identify the two most 'viral' "
        f"or profound moments. Each must be between 30-60 seconds. "
        f"Return ONLY the segments in this format: START-END|HEADLINE "
        f"Example: 12-45|The Secret to Growth. "
        f"Transcript: {full_text}"
    )
    
    response = model.generate_content(prompt)
    raw_text = response.text.strip()
    
    # 3. Parse the output into a format video_processor.py can use
    segments = []
    lines = raw_text.split('\n')
    for line in lines:
        try:
            # Matches format: 10-40|My Awesome Title
            match = re.match(r"(\d+)-(\d+)\|(.*)", line)
            if match:
                segments.append({
                    "start": int(match.group(1)),
                    "end": int(match.group(2)),
                    "text": match.group(3)
                })
        except Exception as e:
            print(f"Error parsing line: {line} - {e}")
            
    return segments