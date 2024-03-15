from moviepy.editor import VideoFileClip, CompositeVideoClip, AudioFileClip
from app.utils import logger

logger = logger.getLogger()

def generate_video(video_data):
    global video_id
    video_id = video_data['id']
    
    logger.info(f"Generating video for video_id: {video_id}")
    
    video_file = f'app/storage/{video_data["id"]}/video.mp4'
    voiceover_file = f'app/storage/{video_data["id"]}/audio.mp3'
    
    video_clip = VideoFileClip(video_file, audio=False)
    voiceover_clip = AudioFileClip(voiceover_file)
    
    # Merge two audio and video
    video_clip = video_clip.set_audio(voiceover_clip)
    
    # cut video to match to audio length
    
    
    
    # Save the video
    video_clip.write_videofile(f'app/storage/{video_data["id"]}/final_video.mp4', codec='libx264', audio_codec='aac')