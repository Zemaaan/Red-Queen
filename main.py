#!/usr/bin/env python
import os
import time
from Threads import GlavniProzor, SpeechToText

# Audio recording parameters
STREAMING_LIMIT = 240000  # 4 minutes
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms

RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'

def get_current_time():
    """Return Current Time in MS."""
    return int(round(time.time() * 1000))


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Hrvoje/Downloads/Crvena Kraljica-a019d8541cd9.json"

if __name__ == '__main__':

    GUIDretva = GlavniProzor()
    TTSThread = SpeechToText(GUIDretva)

    GUIDretva.start()
    TTSThread.start()
