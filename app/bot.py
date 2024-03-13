from app.utils import logger
from app.libraries.controller import themoviedb
from app.libraries.controller import database

logger = logger.getLogger()

video_id = None

def start_bot():
    global video_id
    
    logger.info("Bot started")
    ongoing_video_id = database.get_ongoing_video_id()
    
    if ongoing_video_id != None:
        logger.info("Ongoing data already exists in the database")
        video_data = database.get_ongoing_video_details()
    else:
        logger.info("Getting trending movies and tv shows from the database")
        video_data = themoviedb.find_trending_media()
    
    print(video_data)
    
    
    
def stop_bot():
    logger.info("Bot stopped")