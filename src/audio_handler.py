import base64
import tempfile
import os
from audio import AUDIO_BASE64


class AudioHandler:
    def __init__(self):
        self.audio_file = None

    def decode_audio_to_temp(self):
        audio_data = base64.b64decode(AUDIO_BASE64)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_file.write(audio_data)
        temp_file.close()
        self.audio_file = temp_file.name
        return self.audio_file

    def cleanup_audio(self):
        if self.audio_file and os.path.exists(self.audio_file):
            os.remove(self.audio_file)
