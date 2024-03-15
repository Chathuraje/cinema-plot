import requests
from pydub import AudioSegment
from app.utils import logger
from app.utils.config import loadEnv
import json
logger = logger.getLogger()
import os

AUDD_API_KEY = loadEnv().get('AUDD_API_KEY')


def split_audio(file_path, num_segments):
    segments_info = []
    
    audio = AudioSegment.from_file(file_path)
    duration = len(audio)
    segment_duration = duration // num_segments
    segments = []
    
    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = (i + 1) * segment_duration if i < num_segments - 1 else duration
        segment = audio[start_time:end_time]
        segments.append(segment)
        info = {
            'start_second':  start_time / 1000,
            'end_second': end_time / 1000,
            'duration': (end_time - start_time) / 1000,
        }
        segments_info.append(info)
        
        segment.export(f'audio_segment_{i+1}.mp3', format='mp3', codec='libmp3lame')
    return segments, segments_info

def identify_music(api_token, audio_segments, segments_info, return_info=None, market=None):
    results = []
    for i, segment in enumerate(audio_segments):
        endpoint = 'https://api.audd.io/recognize'
        data = {
            'api_token': api_token,
            'return': return_info,
            'market': market
        }
        files = {'file': segment.export(format='mp3', codec='libmp3lame')}
        response = requests.post(endpoint, data=data, files=files)

        if response.status_code == 200:
            result = response.json()
            result['segment_id'] = i + 1  # Add segment ID to the result
            result['start_second'] = segments_info[i]['start_second']
            result['end_second'] = segments_info[i]['end_second']
            result['duration'] = segments_info[i]['duration']
            results.append(result)
        else:
            if response.status_code == "902":
                logger.error(f"Request failed with status code {response.status_code}.: The limit was Reached")
                
            logger.error({'error': f'Request failed with status code {response.status_code}.'})

    return results

def get_segment_count(file_path, segment_duration):
    audio = AudioSegment.from_file(file_path)
    duration = len(audio)
    return duration // (segment_duration * 1000)  # Converting milliseconds to seconds



def filter_songs(songs_details):
    new_data = []
    titles = {}

    # Iterate through each segment
    for segment in songs_details:
        if segment['result']:  # Check if the 'result' field is not null
            title = segment['result']['title']
            if title not in titles:
                segment_info = {
                    "title": segment['result']['title'],
                    "artist": segment['result']['artist'],
                    "album": segment['result']['album'],
                    "release_date": segment['result']['release_date'],
                    "label": segment['result']['label'],
                    "timestamps": [{
                        "start": segment['start_second'],
                        "end": segment['end_second'],
                        "duration": segment['duration']
                    }]
                }
                titles[title] = len(new_data)  # Store the index of the title in new_data
                new_data.append(segment_info)
            else:
                index = titles[title]  # Get the index of the title in new_data
                # Append the timestamp to the existing entry
                new_data[index]['timestamps'].append({
                    "start": segment['start_second'],
                    "end": segment['end_second'],
                    "duration": segment['duration']
                })
                
    return new_data



def find_musics_in_the_audio(video_id, youtube_key):
    json_file_path = f'app/storage/{video_id}/youtube/identified_songs.json'
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            songs_details = json.load(json_file)
            
            if songs_details is not {}:
                logger.info(f"Song details loaded from {json_file_path}")
                return songs_details
    
    video_folder = f'app/storage/{video_id}/youtube/'
    mp3_file_path = f'{video_folder}/{youtube_key}.mp3'
    
    segment_duration = 10
    num_segments = get_segment_count(mp3_file_path, segment_duration)
    logger.info(f"Number of segments: {num_segments}")
    segments, segments_info = split_audio(mp3_file_path, num_segments)

    results = identify_music(AUDD_API_KEY, segments, segments_info)
    songs_details = []
    for segment_data in results:
        data = segment_data['result']
        # print(segment_data)
        if data is not None:
            logger.info(f"Segment {segment_data['segment_id']}: Song Identified - {data['title']}")
            segment_info = {
                'segment_id': segment_data['segment_id'],
                'start_second': segment_data['start_second'],
                'end_second': segment_data['end_second'],
                'duration': segment_data['duration'],
                'result': {
                    'artist': data['artist'],
                    'title': data['title'],
                    'album': data['album'],
                    'release_date': data['release_date'],
                    'label': data['label'],
                    'timecode': data['timecode']
                }
            }
        else:
            logger.info(f"Segment {segment_data['segment_id']}: Song not identified.")
            segment_info = {
                'segment_id': segment_data['segment_id'],
                'start_second': segment_data['start_second'],
                'end_second': segment_data['end_second'],
                'duration': segment_data['duration'],
                'result': None
            }
        songs_details.append(segment_info)
    
    # Save song details to a JSON file
    new_data = filter_songs(songs_details)
    with open(json_file_path, 'w') as json_file:
        json.dump(new_data, json_file, indent=4)
    logger.info(f"Song details saved to {json_file_path}")
    
    return new_data
