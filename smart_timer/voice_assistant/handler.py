from voice_assistant.engine import VoiceEngine


class VoiceAssistantHandler:
    def __init__(self, command):
        self._voice_engine = VoiceEngine(
            "voice_assistant/models/vosk-model-small-en-us-0.15",
            callback= command,
        )

    def run_engine(self):
        try:

            self._voice_engine.start()

            print("Mic on")
            print("Ctrl+C to exit")
            print("Listening...")

            while True:
                pass

        except KeyboardInterrupt:

            print(
                "\nCtrl+C received."
            )

        finally:

            print(
                "Shutting down..."
            )

            self._voice_engine.stop()

            print(
                "Voice engine stopped"
            )

    def stop_engine(self):
        self._voice_engine.stop()