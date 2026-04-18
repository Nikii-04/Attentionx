from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os

def process_video(video_path, segments_data):
    print(f"--- Starting Video Processing ---")
    clip = VideoFileClip(video_path)
    
    # 1. CORRECTED ROTATION
    # Your last attempt (-90) made it upside down. 
    # Changing to 90 will flip it to the correct upright position.
    print(f"Original size: {clip.w}x{clip.h}")
    clip = clip.rotate(90) 
    
    # Recalculate dimensions based on the NEW rotated frame
    w, h = clip.size
    print(f"Rotated size: {w}x{h}")

    # Calculate crop for Vertical 9:16
    target_ratio = 9/16
    target_w = h * target_ratio
    x_center = w / 2
    
    output_files = []
    
    # Fallback to first 30s if data is missing
    if not segments_data or len(segments_data) == 0:
        print("No segments received from AI. Creating a default clip...")
        segments = [{"start": 0, "end": min(30, clip.duration), "text": "Viral Moment"}]
    else:
        segments = segments_data

    for i, seg in enumerate(segments):
        try:
            print(f"Processing Clip {i}: {seg['start']}s to {seg['end']}s")
            
            # 2. Cut and Crop
            subclip = clip.subclip(seg['start'], seg['end'])
            subclip = subclip.crop(x1=x_center - target_w/2, y1=0, x2=x_center + target_w/2, y2=h)
            subclip = subclip.resize(height=1920) 
            
            # 3. Add Headline (Skips if ImageMagick fails)
            try:
                txt = TextClip(
                    seg['text'], 
                    fontsize=70, 
                    color='yellow', 
                    font='Arial', 
                    method='caption', 
                    size=(subclip.w * 0.8, None)
                )
                txt = txt.set_position(('center', 200)).set_duration(subclip.duration)
                final = CompositeVideoClip([subclip, txt])
            except Exception as text_err:
                print(f"TextClip Skip: {text_err}")
                final = subclip 
            
            out_path = f"outputs/viral_clip_{i}.mp4"
            
            final.write_videofile(
                out_path, 
                codec="libx264", 
                audio_codec="aac", 
                fps=24, 
                preset="ultrafast"
            )
            
            output_files.append(out_path)
            
        except Exception as e:
            print(f"Error processing clip {i}: {e}")
            continue
            
    clip.close()
    print(f"--- Finished! Created {len(output_files)} clips ---")
    return output_files