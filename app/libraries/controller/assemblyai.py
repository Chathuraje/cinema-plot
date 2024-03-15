from app.utils import logger
from app.utils.config import loadEnv
import assemblyai as aai
import json

logger = logger.getLogger()
ASSEMBLYAI_API_KEY = loadEnv().get('ASSEMBLYAI_API_KEY')

def initialize_assemblyai():
    try:
        aai.settings.api_key = ASSEMBLYAI_API_KEY
        transcriber = aai.Transcriber()
        
        return transcriber
    except Exception as e:
        logger.error(f"Error initializing AssemblyAI: {e}")
      
        
def generate_transcript(mp3_file_path, transcript_path):
    logger.info(f"Generating transcript from audio file")
    
    transcriber = initialize_assemblyai()
    transcript = transcriber.transcribe(mp3_file_path)

    if transcript.status == aai.TranscriptStatus.error:
        logger.error(f"Error generating transcript")
    else:
        sentences = transcript.get_sentences() # Getting sentences from the transcript
        for sentence in sentences:
            sentence_data = []
            
            for sentence in sentences:
                start_seconds = round(sentence.start / 1000, 3)
                end_seconds = round(sentence.end / 1000, 3)
                duration_seconds = round(end_seconds - start_seconds, 3)
                    
                word_data = {
                    "start": start_seconds,
                    "end": end_seconds,
                    "duration": duration_seconds,
                    "text": sentence.text
                }
                    
                sentence_data.append(word_data)
            
            with open(transcript_path, "w") as json_file:
                json.dump(sentence_data, json_file, indent=4)