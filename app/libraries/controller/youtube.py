
from app.utils import logger
from pathlib import Path
from pytube import YouTube
import os

logger = logger.getLogger()
    
# Code to download youtube video
def download_video(youtube_key, video_id):
    logger.info(f'Downloading youtube video with key: {youtube_key}')
    
    video_folder = f'app/storage/{video_id}'
    video_path = f'{video_folder}/video.mp4'
    
    if Path(video_path).exists():
        logger.info(f'Youtube video already exists for video_id: {video_id}')
        return
    
    yt = YouTube(f'https://www.youtube.com/watch?v={youtube_key}')
    video_stream = yt.streams.get_highest_resolution()
    video_stream.download(output_path=video_folder)
    
    downloaded_file = video_stream.default_filename
    downloaded_file_path = f'{video_folder}/{downloaded_file}'
    os.rename(downloaded_file_path, video_path)
    
    logger.info(f'Youtube video downloaded for video_id: {video_id}')
    
    return video_path