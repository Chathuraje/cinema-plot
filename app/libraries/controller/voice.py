import elevenlabs
from app.utils import logger
from app.utils.config import loadEnv
from elevenlabs.api import User
import json
import os

logger = logger.getLogger()

ELEVEN_LABS_API_KEYS = json.loads(loadEnv().get('ELEVEN_LABS_API_KEYS'))

def set_api_key(characters):
    for key in ELEVEN_LABS_API_KEYS:
        if set_api_key_and_check(key, characters):
            return True
    return False

def set_api_key_and_check(key, characters):
    try:
        elevenlabs.set_api_key(key)
        user = User.from_api()
        
        character_count = user.subscription.character_count
        character_limit = user.subscription.character_limit
        
        if character_limit - character_count >= (characters+25):
            logger.info(f"API key set successfully!: character_limit={character_limit}, character_count={character_count}")
            return True
        else:
            logger.warning(f"API key has insufficient character limit: character_limit={character_limit}, character_count={character_count}")
    except Exception as e:
        logger.error(f"Error setting API key: {e}")

    return False


def generate_audio(id, story):
    try:
        audio = elevenlabs.generate(
            text=story,
            voice=elevenlabs.Voice(
                voice_id='alMSnmMfBQWEfTP8MRcX',
                settings=elevenlabs.VoiceSettings(stability=0, similarity_boost=0)
            )
        )
        
        file_path = f'app/storage/{id}/audio.mp3'
        with open(file_path, 'wb') as f:
            f.write(audio)

        return True
    except Exception as e:
        logger.error(f"Error generating audio for {id}: {e}")
        

def generate_voice(video_data, story):
    logger.info("ELEVENLABS: Generating voice...")
    
    file_path = f'app/storage/{video_data["id"]}/audio.mp3'
    if os.path.exists(file_path):
        logger.info("Voice already generated.")
        return
    
    characters = len(story)
    logger.info(f"Generating voice for {video_data['id']} with {characters} characters.")
    
    logger.info("ELEVENLABS: Connecting API")
    success = set_api_key(characters)

    if not success:
        logger.error("All API keys failed. Unable to set a valid API key.")
        return

    generate_audio(video_data['id'],  story)
