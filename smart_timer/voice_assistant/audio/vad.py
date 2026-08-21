import numpy as np

class VoiceActivityDetector:

    def is_talking(audio, threshold = 500.0):
        if audio.size == 0:
            return False

        samples = audio.astype(np.float32)
        rms = np.sqrt(np.mean(samples * samples))
        return rms >= threshold