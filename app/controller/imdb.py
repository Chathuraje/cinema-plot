from app.utils import logger
import requests
from bs4 import BeautifulSoup
from imdb import Cinemagoer

logger = logger.getLogger()


def send_request(request_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    response = requests.get(request_url, headers=headers)
    
    if response.status_code == 200:
        return response
    else:
        logger.error(f"Error fetching data from {request_url}")
        return None

def get_movie_reviews(imdb_id, reviews_list):
    url = f"https://m.imdb.com/title/{imdb_id}/reviews/"
    response = send_request(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        review_containers = soup.find_all('div', class_='imdb-user-review')

        for review in review_containers:
            text = f"{review.find('a', class_='title').text.strip()} - {review.find('div', class_='text').text.strip()}"
            
            rating_container = review.find('div', class_='inline-rating')
            rating_span = rating_container.find('span', class_='rating-other-user-rating')
            rating = rating_span.find('span').text.strip()
            
            details = {
                'content': text,
                'rating': rating
            }
            reviews_list.append(details)
        return reviews_list
    
    else:
        logger.error(f"Error fetching reviews for imdb_id: {imdb_id}")
        
        
def get_imdb_rating(imdb_id):
    url = f"https://www.imdb.com/title/{imdb_id}/ratings/"
    response = send_request(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        imdb_rating = soup.find('span', class_='sc-5931bdee-1 gVydpF')

        if imdb_rating:
            return imdb_rating.text.strip()

    
