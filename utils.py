import librosa
import numpy as np

def get_audio_peaks(video_path):
    y, sr = librosa.load(video_path)
    energy = np.abs(y)
    
    peaks = np.where(energy > np.percentile(energy, 90))[0]
    return peaks