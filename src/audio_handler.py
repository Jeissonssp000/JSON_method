import base64
import tempfile
import pygame
import os
from .audio import AUDIO_BASE64


class AudioHandler:
    def __init__(self):
        pygame.mixer.init()
        self.audio_file = self.decode_audio_to_temp()
        pygame.mixer.music.load(self.audio_file)

    def decode_audio_to_temp(self):
        audio_data = base64.b64decode(AUDIO_BASE64)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_file.write(audio_data)
        temp_file.close()
        return temp_file.name

    def play_audio(self):
        pygame.mixer.music.play()

    def cleanup(self):
        if self.audio_file and os.path.exists(self.audio_file):
            os.remove(self.audio_file)
