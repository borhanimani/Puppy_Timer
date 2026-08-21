import numpy as np

class NoiseCanceller:

    def remove_noise(self, audio_list, threshold=500):
        audio = np.frombuffer(audio_list)
        audio[np.abs(audio) < threshold]
        return audio.tobytes()


