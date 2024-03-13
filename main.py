from app.utils import logger
from app.utils.config import loadConfig
from app import bot

# Setup Logger
logger.setupLogger()
logger = logger.getLogger() 
STAGE = loadConfig().get('STAGE', 'DEVELOPMENT')

def main():
    try:
        logger.info(f"Starting bot... {STAGE}")

        # Start Bot
        bot.start_bot()
    except Exception as e:
        logger.error("Error: %s", e)
        logger.error("Bot failed to start")
    
if __name__ == "__main__":
    main()
