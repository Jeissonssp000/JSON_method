import os
import base64

script_dir = os.path.dirname(os.path.abspath(__file__))
input_audio_file = os.path.join(script_dir, "audio.mp3")
output_python_file = os.path.join(script_dir, "audio.py")

if not os.path.exists(input_audio_file):
    raise FileNotFoundError(f"El archivo de audio no se encontró: {input_audio_file}")

with open(input_audio_file, "rb") as audio_file:
    encoded_string = base64.b64encode(audio_file.read()).decode("utf-8")

with open(output_python_file, "w") as py_file:
    py_file.write('AUDIO_BASE64 = """\n')
    py_file.write(encoded_string)
    py_file.write('\n"""')

print(f"Archivo {output_python_file} generado exitosamente.")
