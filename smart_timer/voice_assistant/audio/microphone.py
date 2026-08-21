from sounddevice import InputStream
from queue import Queue, Full


class MicrophoneManager:

    def __init__(self, samplerate=16000, channels=1, blocksize=1600, audio_queue=Queue):
        self._sample_rate = samplerate
        self._channels = channels
        self._blocksize = blocksize
        self._audio_queue: Queue = audio_queue
        self.stream = InputStream

    def callback(self, indata):
        try:
            self._audio_queue.put_nowait(indata)
        except Full:
            # It means the audio_queue is full and do nothing.
            pass

    def start(self):
        self.stream = InputStream(
            samplerate= self._sample_rate,
            blocksize= self._blocksize,
            channels= self._channels,
            callback= self.callback,
        )

        self.stream.start()

    def stop(self):
        self.stream.stop()
        self.stream.close()

