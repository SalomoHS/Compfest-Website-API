import json
import requests
from .supabaseClient import supabase
from .elevenlabsClient import *
from langchain_core.messages import AIMessage
from urllib.parse import urlparse
import asyncio
from io import BytesIO
import uuid

async def json_parser(state):
    print(state["messages"][-1].content)
    ai_response = None
    for msg in state["messages"]:
        if isinstance(msg, AIMessage):
            ai_response = msg

    temp = ai_response.content\
            .replace("```json","")\
            .replace("```","")\
            .strip()
    # print(f"Attempting to parse: '{temp}'")
    temp = json.loads(temp)
    return {"parsed_ai_response": temp}

async def get_speakers():
    """Get speaker data in Postgres"""
    return supabase\
            .table("Speakers")\
            .select("*")\
            .execute()

async def get_topics():
    """Get topic data in Postgres"""
    return supabase\
            .table("Topics")\
            .select("*")\
            .execute()

async def add_bgm(state):
    data = {
        "timeline": {
            "soundtrack": {
            "src": "https://dbdlxpquyiwpntlsizle.supabase.co/storage/v1/object/public/assets/bgm-music.mp3",
            "effect": "fadeIn",
            "volume": 0.1
            },
            "tracks": [{
            "clips": [{
                "asset": {
            "type": "audio",
            "src": state['result_url'],
            "volume": 1.0
        },
                "start": 0,
                "length": "auto"  
            }]
            }]
        },
        "output": { 
            "format": "mp3","resolution": "sd"
            }
        }
    data_to_json= json.dumps(data)
    
    render = requests.post("https://api.shotstack.io/edit/v1/render",data=data_to_json,headers={
        "Content-Type":"application/json",
        "x-api-key":os.environ['SHOTSTACK']
    })
    render_response = render.json()
    try:
        while True:
            poll = requests.get(f"https://api.shotstack.io/edit/v1/render/{render_response['response']['id']}",headers={
                "Content-Type":"application/json",
                "x-api-key":os.environ['SHOTSTACK']
            })
            poll_response = poll.json()
            isComplete = poll_response['response']['status']
            await asyncio.sleep(2)
            
            if isComplete == 'done':
                get_url = poll_response['response']['url']
                resp = requests.get(get_url)
                file_data = resp.content

                without_bgm_file = urlparse(state['result_url']).path
                file_name = without_bgm_file.split("/")[-1].split(".")[0]+'with-bgm.mp3'

                supabase.storage.from_("customPodcast").upload(file_name,file_data,{
                    "content-type":"audio/mpeg","upsert":"true"
                })
                with_bgm_file = supabase.storage.from_("customPodcast").get_public_url(file_name)
                return {'result_url_with_bgm': with_bgm_file}

            await asyncio.sleep(5)
    except Exception as e:
        print("[SHOTSTACK]",e)
        return {'result_url_with_bgm': state['result_url']}


async def delete_voices(client_num:str):
    api = [
        os.environ['ELEVENLABS_KEY_11'],
        os.environ['ELEVENLABS_KEY_1'],
        os.environ['ELEVENLABS_KEY_2'],
        os.environ['ELEVENLABS_KEY_3'],
        os.environ['ELEVENLABS_KEY_4'],
        os.environ['ELEVENLABS_KEY_5'],
    ]

    toBeDelete = api[client_num]

    try:
        res = requests.get("https://api.elevenlabs.io/v2/voices",headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "xi-api-key": toBeDelete,
            "Content-Type": "application/json",
        })

        for voice in res.json()['voices'][:3]:
            delete = requests.delete(f"https://api.elevenlabs.io/v1/voices/{voice['voice_id']}",headers={
                "xi-api-key": toBeDelete,
                "Content-Type": "application/json",
            })
        
        print("DELETE VOICES")

    except Exception as e:
        raise Exception("Could not delete voices")

async def generate_dialog(state):
    speakers = [x['speakerId'] for x in state["parsed_ai_response"]['Insert_Dialogs']]
    dialogs = [x['dialog'] for x in state["parsed_ai_response"]['Insert_Dialogs']]

    clients = [
        elevenlabs_client_11, elevenlabs_client_1
    ]
    clients_str = [
        "elevenlabs_client_11", "elevenlabs_client_1"
    ]

    error_state = {c: '' for c in clients_str}

    attempt = 0
    while attempt < len(clients):
        try:
            request_ids = []
            audio_buffers = []

            # --- Generate audio for each dialog ---
            for paragraph, speaker in zip(dialogs, speakers):
                limited_request_ids = request_ids[-3:]
                with clients[attempt].text_to_speech.with_raw_response.convert(
                    text=paragraph,
                    voice_id=speaker,
                    model_id="eleven_multilingual_v2",
                    previous_request_ids=limited_request_ids
                ) as response:
                    request_ids.append(response._response.headers.get("request-id"))

                    # --- Handle audio data safely ---
                    if isinstance(response.data, (bytes, bytearray)):
                        audio_data = response.data
                    else:
                        audio_data = b''.join(chunk for chunk in response.data)

                    audio_buffers.append(BytesIO(audio_data))

            # --- Combine audio ---
            combined_stream = BytesIO(b''.join(buf.getvalue() for buf in audio_buffers))
            combined_stream.seek(0)

            # --- Try upload to Supabase with retries ---
            retries = 0
            for _ in range(3):
                try:
                    file_name = f"{uuid.uuid4()}.mp3"
                    supabase.storage.from_("customPodcast").upload(
                        file_name,
                        combined_stream.getvalue(),
                        {
                            "content-type": "audio/mpeg",
                            "upsert": "true"
                        }
                    )
                    # https://dbdlxpquyiwpntlsizle.supabase.co/storage/v1/object/public/podcast/test1.mp3
                    storage = supabase.storage.from_("customPodcast").get_public_url(file_name)
                    return {"result_url": storage}
                except Exception as e:
                    print(f"[Upload Error]: {e}")
                    retries += 1
                    continue

            if retries == 3:
                raise Exception("Upload failed after several retries.")

        except Exception as e:
            client_name = clients_str[attempt]
            error_state[client_name] = str(e)
            print(f"[Client Error] {client_name}: {e}")
            attempt += 1
            continue

    # # --- If all clients fail, log error to Supabase ---
    # try:
    #     supabase.table("Errors").insert(error_state).execute()
    # except Exception as e:
    #     print("[Supabase Insert Error]:", e)


