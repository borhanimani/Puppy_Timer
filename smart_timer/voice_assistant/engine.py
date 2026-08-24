import threading
import queue
import json
from vosk import Model, KaldiRecognizer
from .audio import MicrophoneManager
from .vad import VoiceActivityDetector
import numpy as np
from .config import (
    SAMPLE_RATE,
    BLOCK_SIZE,
    ENERGY_THRESHOLD,
    QUEUE_MAX_SIZE,
    QUEUE_TIMEOUT,
    THREAD_JOIN_TIMEOUT,
)


class VoiceEngine:

    def __init__(self,model_path,callback):
        self.model_path = model_path
        self.callback = callback
        self.running = False
        self.stop_event = threading.Event()
        self.queue = queue.Queue(maxsize=QUEUE_MAX_SIZE)
        self.model = None
        self.recognizer = None
        self.vad = VoiceActivityDetector(threshold=500.0)
        self.audio = MicrophoneManager(self.audio_callback,SAMPLE_RATE,BLOCK_SIZE)
        self.thread = None
        self.lock = threading.Lock()

        # -----------------------------
        # Speech state
        # -----------------------------
        self.speaking = False

        # Number of consecutive silent frames
        self.silence_frames = 0

        # About 1 second with 200 ms blocks
        self.max_silence_frames = 5

    # ==================================================
    # START
    # ==================================================

    def start(self):
        with self.lock:
            if self.running:
                return

            try:
                print("Loading Vosk model...")
                self.model = Model(self.model_path)
                self.recognizer = KaldiRecognizer(self.model,SAMPLE_RATE)
                self.stop_event.clear()
                self.running = True
                self.audio.start()
                self.thread = threading.Thread(target=self.worker,name="VoiceRecognitionThread")
                self.thread.start()

            except Exception:
                self._stop_internal()
                raise

    # ==================================================
    # MICROPHONE CALLBACK
    # ==================================================

    def audio_callback(self,data,frames,time,status):

        if status:
            print(f"Audio status: {status}")

        if not self.running:
            return

        try:
            self.queue.put_nowait(bytes(data))

        except queue.Full:
            pass

    # ==================================================
    # WORKER
    # ==================================================

    def worker(self):

        while not self.stop_event.is_set():
            try:
                data = self.queue.get(timeout=QUEUE_TIMEOUT)

            except queue.Empty:
                continue

            if self.stop_event.is_set():
                break

            if self.recognizer is None:
                break

            try:
                # bytes -> numpy array
                audio = np.frombuffer(data,dtype=np.int16)

                # VAD
                voice_active = self.vad.is_voice_active(audio)

                if voice_active:
                    print("VOICE")

                # Vosk
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text","").strip()

                    if text:
                        self.callback(text)

            except Exception as e:
                print(f"Recognizer error: {e}")

    # ==================================================
    # INTERNAL STOP
    # ==================================================

    def _stop_internal(self):
        self.running = False
        self.stop_event.set()

        # Close microphone FIRST.
        self.audio.stop()

        # Stop recognition thread.
        if self.thread is not None:
            if threading.current_thread() is not self.thread:
                self.thread.join(timeout=THREAD_JOIN_TIMEOUT)
            self.thread = None

        # Clear remaining audio from RAM.
        self._clear_queue()

        # Release Vosk.
        self.recognizer = None
        self.model = None
        self.speaking = False
        self.silence_frames = 0

    # ==================================================
    # PUBLIC STOP
    # ==================================================

    def stop(self):
        with self.lock:
            if not self.running:
                return

            self._stop_internal()

    # ==================================================
    # CLEAR QUEUE
    # ==================================================

    def _clear_queue(self):
        while True:
            try:
                self.queue.get_nowait()
            except queue.Empty:
                break

    # ==================================================
    # CONTEXT MANAGER
    # ==================================================
    def __enter__(self):
        self.start()
        return self

    def __exit__(self,exc_type,exc,tb):
        self.stop()