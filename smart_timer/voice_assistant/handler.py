from .engine import VoiceEngine


class VoiceAssistantHandler:

    def __init__(self, command):

        self._voice_engine = VoiceEngine(
            "voice_assistant/models/vosk-model-small-en-us-0.15",
            callback=command,
        )

    # ==================================================
    # START
    # ==================================================

    def start(self):

        self._voice_engine.start()

    # ==================================================
    # STOP
    # ==================================================

    def stop(self):

        self._voice_engine.stop()

    # ==================================================
    # STATE
    # ==================================================

    def is_running(self):

        return self._voice_engine.running