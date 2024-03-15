from app.utils import logger
from app.libraries.controller import themoviedb
from app.libraries.controller import youtube
from app.libraries.controller import chatgpt
from app.libraries.controller import voice
from app.libraries.controller import video

logger = logger.getLogger()

video_id = None

def start_bot():
    global video_id
    
    logger.info("Bot started")
    video_data = themoviedb.find_trending_media()    
    youtube_key = youtube.download_youtube_video(video_data['youtube'], video_data['id'])
    # story = chatgpt.generate_script(video_data)
    # voice.generate_voice(video_data, story)
    
    # video.generate_video(video_data)
    
    
    
    
def stop_bot():
    logger.info("Bot stopped")