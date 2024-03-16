from app.controller import database
from app.controller import wikipedia
from app.controller import storage
from app.controller import themoviedb
from app.controller import imdb
from app.utils import logger
from app.models.Movie import Movie

logger = logger.getLogger()

def find_trending_movie():
    video_data = database.get_ongoing_video_details()
    if video_data != None:
        logger.info("Ongoing data already exists in the database")
        logger.info(f'Trending video found for video_id: {video_data["id"]} -> Title: {video_data["title"]}')
        
        return video_data["id"]
    
    
    logger.info("Getting trending movies and tv shows from the database")
    uploaded_ids = database.get_uploaded_video_ids()
    
    page = 1
    while True:
        logger.info(f'Getting trending movies from page: {page}')
        
        trending_movies = themoviedb.get_trending_movie(page)
        if trending_movies is None:
            logger.error(f'Error finding trending movies')
            break
        
        for movie in trending_movies:
            try:
                video_id = movie['id']
                
                if video_id in uploaded_ids:
                    logger.info(f'Uploaded video with video_id: {video_id} already exists in the database')
                    continue
                
                movie_info = themoviedb.get_movie_details(video_id)
                title = movie_info['title']
                logger.info(f"Getting details for video_id: {video_id} | title: {title}")
                
                
                images_list = []
                images_list.append(f"https://image.tmdb.org/t/p/original/{movie_info['poster_path']}")
                images_list.append(f"https://image.tmdb.org/t/p/original/{movie_info['poster_path']}")
                    
                spoken_languages = []
                for language in movie_info['spoken_languages']:
                    spoken_languages.append(language['english_name'])
                
                genres_list = []
                for genre in movie_info['genres']:
                    genres_list.append(genre['name'])
                
                comapany_list = []
                for companies in movie_info['production_companies']:
                    comapany_list.append(companies['name'])
                    
                imdb_id = movie_info['imdb_id']
                imdb_rating = imdb.get_imdb_rating(imdb_id)
                
                logger.info('Getting team details for the movie')
                credits = themoviedb.get_movie_credits(video_id)
                
                casts = credits['cast']
                cast_details_list = []
                for cast in casts:
                    if cast["known_for_department"] != "Acting":
                        continue
                    
                    person_details = themoviedb.get_person_details(cast['id'])
                    
                    details = {
                        'name': cast['name'],
                        'character': cast['character'],
                        'image': None,
                        'imdb_id': person_details['imdb_id'],
                    }
                    cast_details_list.append(details)
                    
                    if len(cast_details_list) > 10:
                        break
                    
                crews = credits['crew']
                crew_details_list = []
                for crew in crews:
                    if crew["known_for_department"] != "Directing":
                        continue
                    
                    person_details = themoviedb.get_person_details(cast['id'])
                    
                    details = {
                        'name': crew['name'],
                        'job': crew['job'],
                        'image': None,
                        'imdb_id': person_details['imdb_id'],
                    }
                    if len(crew_details_list) > 10:
                        break
                
                    crew_details_list.append(details)
                    
                team_list = {
                    'cast': cast_details_list,
                    'crew': crew_details_list
                }
                    
                logger.info('Getting keywords for the movie')
                keywords = themoviedb.get_movie_keywords(video_id)
                keywords_list = []
                for keyword in keywords["keywords"]:
                    keywords_list.append(keyword['name'])
                    
                
                logger.info('Getting Reviews for the movie')
                reviews = themoviedb.get_movie_reviews(video_id)
                reviews_list = []
                for review in reviews['results']:
                    details = {
                        'content': review['content'],
                        'rating': review['author_details']['rating']
                    }
                    reviews_list.append(details)
                    
                if movie_info['imdb_id'] is not None:
                    reviews = imdb.get_movie_reviews(movie_info['imdb_id'], reviews_list)
                    if len(reviews) > 0:
                        reviews_list = reviews
                    
                logger.info("Getting videos for the movie")
                videos = themoviedb.get_movie_videos(video_id)
                videos_list = []
                for video in videos['results']:
                    if video['site'] == 'YouTube' and video['official']:
                        if video['type'] == 'Trailer' or video['type'] == 'Teaser' or video['type'] == 'Clip':
                            video_info = {
                                'key': video['key'],
                                'type': video['type'],
                                'transcript': None
                            }
                            videos_list.append(video_info)
                
                logger.info('Getting plot and cast details for the movie')
                movie_details = wikipedia.get_movie_details(movie_info['title'], movie_info['release_date'])
                if movie_details is not None:
                    plot = movie_details.get('plot')
                    cast_details = movie_details.get('cast')
                else:
                    plot = None
                    cast_details = None
                    logger.info(f'Error getting plot and cast details for the movie')
                    
                
                selcted_movie = Movie(
                    unique_id = video_id,
                    title = title,
                    original_language = movie_info['original_language'],
                    overview = movie_info['overview'],
                    media_type = 'movie',
                    genres = genres_list,
                    release_date = movie_info['release_date'],
                    budget = movie_info['budget'],
                    imdb_id = imdb_id,
                    imdb_rating = imdb_rating,
                    production_companies = comapany_list,
                    revenue = movie_info['revenue'],
                    runtime = movie_info['runtime'],
                    spoken_languages = spoken_languages,
                    status = movie_info['status'],
                    team = team_list,
                    cast_details = cast_details,
                    reviews = reviews_list, 
                    images = images_list,
                    keywords = keywords_list,
                    videos = videos_list,
                    plot= plot
                )
                
                logger.info(f'Video selected: {video_id} | title: {title}')
                
                storage.create_folders(video_id)
                database.store_ongoing_video_data(selcted_movie)
                return video_id
            
            except Exception as e:
                logger.error(f'Error finding trending movies: {e}')
                continue
        
        page += 1
    
        