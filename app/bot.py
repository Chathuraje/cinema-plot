from app.utils import logger
from app.libraries import collect_data

logger = logger.getLogger()

def start_bot():
    logger.info("Bot started")
    video_id = collect_data.find_trending_movie()
    
    
    
def stop_bot():
    logger.info("Bot stopped")