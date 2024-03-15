from openai import OpenAI
from app.utils import logger
from app.utils.config import loadEnv
import os
import json

logger = logger.getLogger()
OPENAPI_API_KEY = loadEnv().get('OPENAPI_API_KEY')


def initialize_openai():
    try:
        client = OpenAI(
            api_key = OPENAPI_API_KEY,
        )
        
        return client
    except Exception as e:
        logger.error(f"Error initializing OpenAI: {e}")

def generate_chat_completion(client, messages):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        response = completion.choices[0].message.content
        is_done = completion.choices[0].finish_reason != 'stop'
        return response, is_done

    except Exception as e:
        logger.error(f"Error generating GPT: {e}")
        return None

def ask_gpt(client, prompt, conversation):
    conversation.append({'role': 'user', 'content': prompt})
    response, is_done = generate_chat_completion(client, conversation)
    
    return response, is_done

def ask(client, prompt, conversation=[]):
    response = None
    is_done = True
    
    while response is None or is_done:
        logger.info(f"Waiting for conversation...")
        response, is_done = ask_gpt(client, prompt, conversation)
    
    output = response.replace('"', '')
    
    return output


def generate_script(video_data):
    file_path = f'app/storage/{video_data["id"]}/story.txt'
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            story = file.read()
            if story != '':
                logger.info(f"Story Found in Storage")
                return story
                
    
    client = initialize_openai()
    conversation = [
        {
            "role": "system",
            "content": "You will be provided with a movie plot and the title of it.  \n Craft a engaging summarize story to 250 words that suitable for a YouTube video that aims to captivate the viewer's curiosity and enjoyment without revealing any spoilers. Utilize the plot elements provided from the specified movie but infuse the narrative with a more serious tone and enhance its emotional resonance to make it more endearing.\n"
        },
        {
            "role": "user",
            "content": "Title: Oppenheimer\n\nPlot: The film is presented as a nonlinear narrative, with two different timelines interwoven together. The first is \"Fission\", playing out in color, about Oppenheimer giving a subjective account of his life at his 1954 security hearing, while the second is \"Fusion\", in black and white, which is Lewis Strauss's viewpoint on Oppenheimer during his 1959 Senate confirmation hearing. The plot summary is linear. In 1926, 22-year-old doctoral student J. Robert Oppenheimer grapples with anxiety and homesickness while studying experimental physics under Patrick Blackett at the Cavendish Laboratory in the University of Cambridge. Upset with Blackett's attitude, Oppenheimer leaves him a poisoned apple but later retrieves it. Visiting scientist Niels Bohr advises Oppenheimer to study theoretical physics at the University of Göttingen instead. Oppenheimer completes his PhD there and meets fellow scientist Isidor Isaac Rabi. They later meet theoretical physicist Werner Heisenberg in Switzerland. Wanting to expand quantum physics research in the United States, Oppenheimer begins teaching at the University of California, Berkeley and the California Institute of Technology. He marries Katherine \"Kitty\" Puening, a biologist and ex-communist, and has an intermittent affair with Jean Tatlock, a troubled communist psychiatrist who later dies by suicide. When nuclear fission is discovered in 1938, Oppenheimer realizes it could be weaponized. In 1942, during World War II, US Army Colonel Leslie Groves, director of the Manhattan Project, recruits Oppenheimer as director of the Los Alamos Laboratory, where an atomic bomb is to be developed. Oppenheimer fears the German nuclear research program, led by Heisenberg, might yield a fission bomb for the Nazis. He assembles a team consisting of Rabi, Hans Bethe, and Edward Teller at the Los Alamos Laboratory, and also collaborates with scientists Enrico Fermi, Leo Szilard, and David L. Hill at the University of Chicago. Teller's calculations reveal an atomic detonation could trigger a catastrophic chain reaction that would ignite the atmosphere and destroy the world. After consulting with Albert Einstein, Oppenheimer concludes the chances are acceptably low. Teller attempts to leave the project after his proposal to construct a hydrogen bomb is rejected, but Oppenheimer convinces him to stay. After Germany's surrender in 1945, some Project scientists question the bomb's relevance. Oppenheimer believes it would end the ongoing Pacific War and save Allied lives. The Trinity test is successful, and President Harry S. Truman orders the atomic bombings of Hiroshima and Nagasaki, resulting in Japan's surrender. Though publicly praised, Oppenheimer is haunted by the mass destruction and fatalities. After Oppenheimer expresses his personal guilt in a private meeting with Truman, the president berates Oppenheimer and dismisses his urging to cease further atomic development. As an advisor to the United States Atomic Energy Commission (AEC), Oppenheimer's stance generates controversy, while Teller's hydrogen bomb receives renewed interest amidst the burgeoning Cold War. AEC Chairman Lewis Strauss resents Oppenheimer for publicly dismissing Strauss's concerns about exporting radioisotopes and for recommending negotiations with the Soviet Union after the Soviets successfully detonated their own bomb. Strauss also believes that Oppenheimer denigrated him during a conversation Oppenheimer had with Einstein in 1947. In 1954, wanting to eliminate Oppenheimer's political influence, Strauss secretly orchestrates a private security hearing before a Personnel Security Board concerning Oppenheimer's Q clearance. However, it becomes clear that the hearing has a predetermined outcome. Oppenheimer's past communist ties are exploited, and Groves's, Teller's, and other associates' testimony is twisted against Oppenheimer. After Kitty gives an impassioned testimony calling this out, the board chooses to uphold Oppenheimer's citizenship but revokes Oppenheimer's clearance, damaging Oppenheimer's public image and limiting his influence on nuclear policy. In 1959, during Strauss's Senate confirmation hearing for Secretary of Commerce, Hill testifies about Strauss's personal motives in engineering Oppenheimer's downfall, resulting in Strauss's nomination being voted down. In 1963, President Lyndon B. Johnson presents Oppenheimer with the Enrico Fermi Award as a gesture of political rehabilitation. A flashback reveals that Oppenheimer and Einstein's 1947 conversation never mentioned Strauss. Instead, the two discussed Oppenheimer’s legacy, and Oppenheimer expressed his fear that they had indeed started a chain reaction – that being a nuclear arms-race{{snd]] that will one day destroy the world. As Einstein leaves, Oppenheimer imagines a world being consumed by nuclear fire, before he closes his eyes in despair."
        },
        {
            "role": "assistant",
            "content": "In a mesmerizing tale of brilliance and regret, \"Oppenheimer\" delves into the life of J. Robert Oppenheimer, the father of the atomic bomb. Follow his journey from academic struggles in Cambridge to the pivotal role he played in the Manhattan Project during World War II. Witness the moral dilemmas he faced, the personal sacrifices made, and the haunting aftermath of the bombings in Japan. As Oppenheimer grapples with his conscience and faces political persecution, his legacy becomes a poignant reminder of the destructive power he helped unleash. Experience the gripping narrative of a man torn between duty and humanity, as the shadows of his past come back to haunt him, echoing a chilling prophecy of a world on the brink of annihilation. Join us on a gripping odyssey through a troubled genius's tumultuous life, filled with passion, betrayal, and the weight of a world forever changed by his actions."
        }
    ]
    prompt = f"""Title: {video_data['title']}\n\nPlot: {video_data['plot']}"""
    story = ask(client, prompt, conversation)
    
    with open(file_path, 'w') as file:
        file.write(story)
        
        logger.info(f"Story Generated: {story}")
    
    return story


def generate_transcript(audio_file, transcript_path):
    logger.info(f"Generating transcript from audio file")
    
    client = initialize_openai()
    
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="srt"
    )
    
    print(transcription)

    segment_list = []
    text = ""
    for segment in transcription.segments:
        start_time = segment['start']
        end_time = segment['end']
        if text == segment['text']:
            continue
        text = segment['text']
        duration = end_time - start_time
        segment_list.append({
            "start": start_time,
            "end": end_time,
            "duration": duration,
            "text": text
        })

    print(segment_list)
    
    # return transcript
    # with open(transcript_path, 'w') as f:
    #     json.dump(segment_list, f, indent=4)
    
        