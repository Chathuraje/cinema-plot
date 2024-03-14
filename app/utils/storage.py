from pathlib import Path
from app.utils import logger

logger = logger.getLogger()

def create_folders(video_id):
    subdirectory_names = ['data']
    
    folder_path = Path(f'app/storage/{video_id}')
    if not folder_path.exists():
        logger.info(f'Creating folder: {folder_path}')
        folder_path.mkdir(parents=True, exist_ok=True)
    
    for name in subdirectory_names:
        subdirectory = folder_path / name
        if not subdirectory.exists():
            logger.info(f'Creating subfolder: {subdirectory}')
            subdirectory.mkdir(parents=True, exist_ok=True)