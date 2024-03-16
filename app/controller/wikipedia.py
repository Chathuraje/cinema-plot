import requests
from app.utils.config import loadEnv
from app.utils import logger
import json
import wikipediaapi
import unicodedata

logger = logger.getLogger()
WIKEPEDIA_USER_AGENT = loadEnv().get('WIKEPEDIA_USER_AGENT')


def normalize_text(text):
    return unicodedata.normalize('NFC', text)

def search_movie(search_query):
    number_of_results = 5
    headers = {
    # 'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
    'User-Agent': WIKEPEDIA_USER_AGENT
    }

    url = f'https://api.wikimedia.org/core/v1/wikipedia/en/search/page'
    parameters = {'q': search_query, 'limit': number_of_results}
    response = requests.get(url, headers=headers, params=parameters)
    
    if response.status_code == 200:
        response_json = json.loads(response.text)
        if len(response_json['pages']) > 0:
            page_keys = []
            for page in response_json['pages']:
                page_keys.append(page['key'])
                
            logger.info(f'Wikipedia search results: {page_keys}')
            return page_keys
        else:
            logger.error(f'Wikipedia search results failed: {response_json}')
            return None
        
    logger.error(f'Wikipedia search results failed: {response.status_code}')
    return None


def get_movie_details(movie_name, release_date):
    movie_info = {"plot": None, "cast": None}
    
    if release_date is not None:
        movie_name = f"{movie_name} {release_date[:4]}"
    
    logger.info(f"Searching for movie details using Wikipedia: {movie_name}")
    keys = search_movie(movie_name)
    
    if keys is None:
        return None
    
    for key in keys:
        logger.info(f"Getting details for: {key}")
        wiki = wikipediaapi.Wikipedia(WIKEPEDIA_USER_AGENT, 'en')

        search_result = wiki.page(key)
        if search_result.exists():
            logger.info(f"Page exists: {key}")
            page_content = search_result.text
            
            # Extract plot
            plot_index = page_content.find("Plot")
            if plot_index != -1:
                logger.info(f"Plot found for: {key}")
                end_index = page_content.find("\n\n", plot_index)
                plot_section = page_content[plot_index:end_index]

                plot_section_lines = plot_section.split('\n')
                if len(plot_section_lines) > 1 and plot_section_lines[0].strip().lower() == 'plot':
                    plot_section = ' '.join(plot_section_lines[1:])
                    
                movie_info["plot"] = normalize_text(plot_section)
            else:
                logger.error(f"Plot not found for: {key}")
            
            # Extract cast
            cast_index = page_content.find("Cast")
            if cast_index != -1:
                logger.info(f"Cast found for: {key}")
                end_index = page_content.find("\n\n", cast_index)
                cast_section = page_content[cast_index:end_index]

                cast_section_lines = cast_section.split('\n')
                if len(cast_section_lines) > 1 and cast_section_lines[0].strip().lower() == 'cast':
                    cast_section_lines = cast_section_lines[1:]
                    
                # Append each line of the cast section to the cast_list
                cast_list = []
                for line in cast_section_lines:
                    cast_list.append(normalize_text(line))
                    
                movie_info["cast"] = cast_list
                
            return movie_info  # Return the dictionary containing plot and cast details
            
        else:
            logger.error(f"Page does not exist: {key}")
            return None
