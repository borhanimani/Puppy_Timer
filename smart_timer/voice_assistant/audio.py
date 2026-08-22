import sounddevice as sd


class MicrophoneManager:

    def __init__(self,callback,samplerate,blocksize):
        self.callback = callback
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.stream = None

    def start(self):
        if self.stream is not None:
            return

        try:
            self.stream = sd.RawInputStream(
                samplerate=self.samplerate,
                blocksize=self.blocksize,
                dtype="int16",
                channels=1,
                callback=self.callback
            )

            self.stream.start()

        except Exception:
            self.stop()
            raise

    def stop(self):
        if self.stream is None:
            return

        try:
            self.stream.stop()
            self.stream.close()
            
        except Exception as e:
            print(f"Microphone cleanup error: {e}")

        self.stream = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()