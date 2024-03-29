from app.utils import mongodb
from app.utils import logger

logger = logger.getLogger()

def get_uploaded_video_ids():
    logger.info("Loading uploaded video data")
    videos_collection = mongodb.get_collection("videos_collection")
    
    video_ids = []
    for video in videos_collection.find():
        video_ids.append(video['unique_id'])
    
    return video_ids

def get_ongoing_video_details():
    ongoing_collection = mongodb.get_collection("ongoing_collection")
    
    ongoing_data = ongoing_collection.find_one()
    
    return ongoing_data


def store_ongoing_video_data(selcted_movie):
    ongoing_collection = mongodb.get_collection("ongoing_collection")
    ongoing_collection.insert_one(selcted_movie.dict())
    
    return True

def clear_ongoing_video_data():
    ongoing_collection = mongodb.get_collection("ongoing_collection")
    ongoing_collection.delete_many({})
    
    return True


def store_video_data(data):
    videos_collection = mongodb.get_collection("videos_collection")
    
    data_list = [data]
    videos_collection.insert_many(data_list)
    
    return True