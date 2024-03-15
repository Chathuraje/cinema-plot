
from app.utils import logger
from pathlib import Path
from pytube import YouTube
import os
from app.libraries.controller import assemblyai
import json

logger = logger.getLogger()

def download_youtube_video(youtube_key, video_id):
    logger.info(f'Downloading youtube video with key: {youtube_key}')
    
    video_folder = f'app/storage/{video_id}/youtube/'
    mp3_file_path = f'{video_folder}/{youtube_key}.mp3'
    mp4_file_path = f'{video_folder}/{youtube_key}.mp4'
    
    if Path(mp3_file_path).exists() and Path(mp4_file_path).exists():
        logger.info(f'Youtube video and audio already downloaded for video_id: {video_id}')
    else:
        yt = YouTube(f'https://www.youtube.com/watch?v={youtube_key}')
        
        logger.info(f'Downloading video for video_id: {video_id}')
        filter_for_video = yt.streams.filter(progressive=False, only_video=True).asc().first()
        filter_for_video.download(output_path=video_folder, filename=f"{youtube_key}.mp4")
        
        logger.info(f'Downloading audio for video_id: {video_id}')
        filter_for_audio = yt.streams.filter(progressive=False, only_audio=True).asc().first()
        filter_for_audio.download(output_path=video_folder, filename=f"{youtube_key}.mp3")
        
        logger.info(f'Youtube video downloaded for video_id: {video_id}')
        
    transcript_file = os.path.join(video_folder, f'{youtube_key}.json')
    if not Path(transcript_file).exists():
        logger.info(f'Generating transcript for youtube video with key: {youtube_key}')
        
        # transcript = get_youtube_transcript_from_yt(youtube_key, transcript_file)
        # if transcript == None:
            # transcript = assemblyai.generate_transcript(mp3_file_path, transcript_file)
        assemblyai.generate_transcript(mp3_file_path, transcript_file)
        
    else:
        logger.info(f'Transcript already generated for video_id: {video_id}')
    
    return youtube_key

from youtube_transcript_api import YouTubeTranscriptApi


# def remove_unnecessary_elements(text):
#     if text == None:
#         return None
    
#     if text.find('♪') != -1:
#         return None
    
#     text = text.replace('\n', ' ')
#     text = text.replace('...', ' ')
#     text = text.replace('..', ' ')
#     text = text.replace('[*]', ' ')
    
#     speaker_pattern = r'\b[Ss]peaker \d+[:\s]*|\b[Ii]nterviewer[:\s]*'
#     text = re.sub(speaker_pattern, '', text)
    
#     return text


# def format_scrape_text(fetched_transcript, transcript_path):
#     formatted_data = []
#     for entry in fetched_transcript:
#         end_time = entry['start'] + entry['duration']
#         formatted_entry = {
#             'start': entry['start'],
#             'end': end_time,
#             'duration': entry['duration'],
#             'text': entry['text']
#         }
#         formatted_data.append(formatted_entry)
    
#     with open(transcript_path, "w") as json_file:
#         json.dump(formatted_data, json_file, indent=4)
    
#     return formatted_data


# def get_youtube_transcript_from_yt(video_id, transcript_file):
#     try:
#         transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
#         for transcript in transcript_list:
#             if (transcript.is_generated == False):
#                 language_code_list = ['en', 'en-US', 'en-AU', 'en-CA', 'en-UK']
#                 if transcript.language_code in language_code_list:
#                     logger.info("Getting youtube transcript from Youtube")
                    
#                     return format_scrape_text(transcript.fetch(), transcript_file)
                    
#     except Exception as e:
#         print(f'Error getting transcript: {e}')
#         return None