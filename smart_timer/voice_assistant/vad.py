import numpy as np


class VoiceActivityDetector:

    def __init__(self, threshold: float = 500.0):
        self.threshold = threshold

    def is_voice_active(self, audio: np.ndarray) -> bool:

        if audio.size == 0:
            return False

        samples = audio.astype(np.float32)

        rms = np.sqrt(
            np.mean(samples * samples)
        )

        return rms >= self.threshold