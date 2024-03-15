from app.utils import logger
from app.libraries.controller import themoviedb
from app.libraries.controller import youtube
from app.libraries.controller import chatgpt
from app.libraries.controller import voice
from app.libraries.controller import video
from app.libraries.controller import database
from app.libraries.controller import songidentifier

logger = logger.getLogger()

video_data = None

def start_bot():
    global video_data
    
    logger.info("Bot started")
    video_data = themoviedb.find_trending_media()    
    youtube.download_youtube_video(video_data['youtube'], video_data['id'])
    songs = songidentifier.find_musics_in_the_audio(video_data['id'], video_data['youtube'])

    # story = chatgpt.generate_script(video_data)
    # voice.generate_voice(video_data, story)
    
    # video.generate_video(video_data)
    
    # database.store_video_data(video_data)
    # database.clear_ongoing_video_data()
    
    
    
    
def stop_bot():
    logger.info("Bot stopped")