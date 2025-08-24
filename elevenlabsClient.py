from elevenlabs import ElevenLabs
import os
from dotenv import load_dotenv
load_dotenv()

elevenlabs_client_1 = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_KEY_1"),
)

elevenlabs_client_2 = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_KEY_2"),
)

elevenlabs_client_3 = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_KEY_3"),
)

elevenlabs_client_4 = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_KEY_4"),
)

elevenlabs_client_11 = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_KEY_11"),
)