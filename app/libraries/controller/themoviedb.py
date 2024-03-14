import requests
from app.utils import logger
from app.utils.config import loadEnv
import json
from app.libraries.controller import database
from app.libraries.controller import wikipedia
from app.utils import storage

logger = logger.getLogger()

TMDB_READ_ACCESS_TOKEN = loadEnv().get('TMDB_READ_ACCESS_TOKEN')

def send_request(url):
    try:
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + TMDB_READ_ACCESS_TOKEN
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        logger.info(f"Url: {url} - Request sent successfully")
        return json.loads(response.text)
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending request: {e}")
        raise RuntimeError(f"Error sending request: {e}")
    
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response: {e}")
        raise RuntimeError(f"Error decoding JSON response: {e}")

def authentication():
    url = "https://api.themoviedb.org/3/authentication/"
    return send_request(url)

def get_trending_media(page=1):
    trending_url = f"https://api.themoviedb.org/3/trending/all/day?language=en-US&page={page}"
    trending_response = send_request(trending_url)
    
    return trending_response['results']

def get_video_details(media_type, video_id):
    video_details_url = f"https://api.themoviedb.org/3/{media_type}/{video_id}/videos?language=en-US"
    video_details = send_request(video_details_url)
    
    for result in video_details['results']:
        if result.get('type') == 'Trailer' and result.get('official') and result.get('site') == 'YouTube':
            return result['key']
        
    return None
            
def get_video_keywords(media_type, video_id):
    keywords_url = f"https://api.themoviedb.org/3/{media_type}/{video_id}/keywords?language=en-US"
    keywords = send_request(keywords_url)
    
    if "keywords" in keywords:  # Check if it's a movie
        return [keyword["name"] for keyword in keywords["keywords"]]
    elif "results" in keywords:  # Check if it's a TV show
        return [tag["name"] for tag in keywords["results"]]
    else:
        return None

def is_valid_trending_media(media):
    required_fields = ['id', 'overview', 'media_type']
    if media.get('media_type') == 'movie':
        required_fields.append('title')
        required_fields.append('release_date')
    elif media.get('media_type') == 'tv':
        required_fields.append('name')
        required_fields.append('first_air_date')
        
    return all(field in media for field in required_fields)

def find_trending_media():
    video_data = database.get_ongoing_video_details()
    if video_data != None:
        logger.info("Ongoing data already exists in the database")
        logger.info(f'Trending video found for video_id: {video_data["id"]} | media_type: {video_data["media_type"]} -> Title: {video_data["title"]}')
        
        return video_data
    
    
    logger.info("Getting trending movies and tv shows from the database")
    page = 1
    uploaded_ids = database.get_uploaded_video_datas()
    
    while True:
        trending_media = get_trending_media(page)
                
        for result in trending_media:
            title = result['title'] if result['media_type'] == 'movie' else result['name']
            
            logger.info(f'Trending video found for video_id: {result["id"]} | media_type: {result["media_type"]} -> Title: {title}')
            if not is_valid_trending_media(result):
                logger.error(f'Invalid trending media: {result}')
                continue
            
            video_id = result['id']
            if video_id in uploaded_ids:
                logger.info(f'Uploaded video with video_id: {video_id} already exists in the database')
                continue
            
            overview = result['overview']
            release_date = result['release_date'] if result['media_type'] == 'movie' else result['first_air_date']
            
            media_type = result['media_type']
            if media_type not in ['movie', 'tv']:
                logger.error(f'Invalid media type: {media_type}')
                continue
            
            youtube_key = get_video_details(media_type, video_id)
            if youtube_key is None:
                logger.error(f'Youtube key not found for video_id: {video_id}')
                continue
            
            keywords = get_video_keywords(media_type, video_id)
            if keywords is None:
                logger.error(f'Keywords not found for video_id: {video_id}')
                continue
            
            plot = wikipedia.get_movie_plot(title, release_date)
            if plot is None:
                logger.error(f'Plot not found for video_id: {video_id}')
                continue
            
            logger.info(f'Video selected: {video_id} | title: {title}')
            
            info = {
                'id': video_id,
                'title': title,
                'overview': overview,
                'media_type': media_type,
                'release_date': release_date,
                'youtube': youtube_key,
                'keywords': keywords,
                'plot': plot
            }
            
            storage.create_folders(info['id'])
            return database.store_ongoing_video_data(info)
        page += 1