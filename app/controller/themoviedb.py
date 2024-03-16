import requests
from app.utils import logger
from app.utils.config import loadEnv
import json

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
        
        return json.loads(response.text)
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending request: {e}")
        raise RuntimeError(f"Error sending request: {e}")
    
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response: {e}")
        raise RuntimeError(f"Error decoding JSON response: {e}")

def get_trending_movie(page=1):
    trending_url = f"https://api.themoviedb.org/3/trending/movie/day?language=en-US&page={page}"
    trending_response = send_request(trending_url)
    
    return trending_response['results']

def get_movie_details(video_id):
    video_details_url = f"https://api.themoviedb.org/3/movie/{video_id}?language=en-US"
    video_details = send_request(video_details_url)
        
    return video_details

def get_movie_credits(video_id):
    credits_url = f"https://api.themoviedb.org/3/movie/{video_id}/credits?language=en-US"
    credits = send_request(credits_url)
    
    return credits
            
def get_movie_keywords(video_id):
    keywords_url = f"https://api.themoviedb.org/3/movie/{video_id}/keywords?language=en-US"
    keywords = send_request(keywords_url)
   
    return keywords

def get_movie_reviews(video_id):
    reviews_url = f"https://api.themoviedb.org/3/movie/{video_id}/reviews?language=en-US"
    reviews = send_request(reviews_url)
    
    return reviews

def get_movie_videos(video_id):
    videos_url = f"https://api.themoviedb.org/3/movie/{video_id}/videos?language=en-US"
    videos = send_request(videos_url)
    
    return videos

def get_person_details(person_id):
    people_url = f"https://api.themoviedb.org/3/person/{person_id}?language=en-US"
    people = send_request(people_url)
    
    return people