from voice_assistant.handler import VoiceAssistantHandler
from controller.keywords import WAKE_WORDS

class WakeWordController:
    def __init__(self, on_wake_word):
        self._voice_assisstant_handler = None
        self._on_wake_word = on_wake_word

    def check_word(self,text):
        words = text.lower().split(' ')
        for word in words:
            if word in WAKE_WORDS:
                self.stop_wake_word()

                if self._on_wake_word:
                    self._on_wake_word()

                return


    def load_assistant(self):
        self._voice_assisstant_handler = VoiceAssistantHandler(self.check_word)
        self._voice_assisstant_handler.run_engine()

    def stop_wake_word(self):
        if self._voice_assisstant_handler:
            self._voice_assisstant_handler.stop_engine()
            self._voice_assisstant_handler = None