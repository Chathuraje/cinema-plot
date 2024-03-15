from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums

def generate_video(video_data):
    global video_id
    video_id = video_data['id']
    
    
    video_file = f'app/storage/{video_data["id"]}/video.mp4'
    audio_file = f'app/storage/{video_data["id"]}/audio.mp3'
    
    video_clip = VideoFileClip(video_file, audio=False)
    
    # Extract audio from video clip
    audio_clip = video_clip.audio
    
    # Write audio to a separate file
    audio_clip.write_audiofile(audio_file)
    
    # Transcribe audio to text
    subtitles_text = transcribe_audio(audio_file)
    
    # Create subtitle clip
    subtitle_text = '\n'.join(subtitles_text)  # Join transcript into a single string
    subtitle_duration = video_clip.duration
    subtitle_clip = TextClip(subtitle_text, fontsize=40, color='white', font='Arial', size=video_clip.size)
    subtitle_clip = subtitle_clip.set_duration(subtitle_duration).set_position('center')
    
    # Composite the subtitle onto the video
    final_video_clip = CompositeVideoClip([video_clip, subtitle_clip])
    
    # Save the video
    final_video_clip.write_videofile(f'app/storage/{video_data["id"]}/final_video.mp4', codec='libx264', audio_codec='aac')

def transcribe_audio(audio_file):
    client = speech.SpeechClient()

    # Load audio file
    with open(audio_file, "rb") as audio_file:
        content = audio_file.read()

    audio = {"content": content}

    config = {
        "language_code": "en-US",
        "enable_automatic_punctuation": True,
        "audio_channel_count": 2,  # Adjust according to your audio
    }

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    subtitles_text = []
    for result in response.results:
        subtitles_text.append(result.alternatives[0].transcript)

    return subtitles_text
