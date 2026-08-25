from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOUND_DIR = BASE_DIR / "sounds"

# Sound Library:

# 1. Add your sound into "assets/sounds" folder. (if the "sounds" does not exist, make a folder "sounds").
# 2. If you want to change and use the sounds, you can change the ("work.way") with your ("example.wav").
# 3. The suggestion:
# - The sounds format need to be: (.wav), you should change the codes for any other format.
# - The sounds' time duration better be less than 2 seconds or 3 seconds.

WAV_WORK_SOUND = SOUND_DIR / "work.wav"
WAV_FINISH_SOUND = SOUND_DIR / "finish.wav"
WAV_WAKE_SOUND = SOUND_DIR / "wake_word.wav"