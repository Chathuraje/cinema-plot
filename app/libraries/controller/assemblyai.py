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
    logger.info("Generating transcript from audio file")
    
    transcriber = initialize_assemblyai()
    transcript = transcriber.transcribe(mp3_file_path)

    if transcript.status == aai.TranscriptStatus.error:
        logger.error("Error generating transcript")
    else:
        sentences = transcript.get_sentences() # Getting sentences from the transcript
        for sentence in sentences:
            sentences_data = []
            
            for sentence in sentences:
                start_seconds = sentence.start
                end_seconds = sentence.end
                duration_seconds = (end_seconds - start_seconds)
                
                words = sentence.words
                words_data = []
                total_word_duration = 0
                
                for word in words:
                    word_start_seconds = word.start
                    word_end_seconds = word.end
                    word_duration_seconds = (word_end_seconds - word_start_seconds)
                    
                    word_data = {
                        "start": word_start_seconds,
                        "end": word_end_seconds,
                        "duration": word_duration_seconds,
                        "text": word.text
                    }
                    words_data.append(word_data)
                
                # Add total word duration for the sentence
                data = {
                    "start": start_seconds,
                    "end": end_seconds,
                    "duration": duration_seconds,
                    "text": sentence.text,
                    "words": words_data,
                }
                    
                sentences_data.append(data)
            
            with open(transcript_path, "w") as json_file:
                json.dump(sentences_data, json_file, indent=4)