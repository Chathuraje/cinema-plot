from app.utils import logger
from app.libraries.controller import themoviedb
from app.libraries.controller import youtube

logger = logger.getLogger()

video_id = None

def start_bot():
    global video_id
    
    logger.info("Bot started")
    video_data = themoviedb.find_trending_media()    
    
    youtube.download_video(video_data['youtube'], video_data['id'])
    
    
    
    
def stop_bot():
    logger.info("Bot stopped")