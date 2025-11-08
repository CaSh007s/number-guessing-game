import os
import simpleaudio as sa
from threading import Thread

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "../platforms/gui/assets")

def play_sound(filename: str):
    path = os.path.join(ASSETS_PATH, filename)
    if not os.path.exists(path):
        return  # Silent fail
    try:
        wave_obj = sa.WaveObject.from_wave_file(path)
        Thread(target=wave_obj.play, daemon=True).start()
    except:
        pass  # Ignore sound errors