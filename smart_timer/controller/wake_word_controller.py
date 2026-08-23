from voice_assistant.handler import VoiceAssistantHandler
from controller.keywords import WAKE_WORDS

class WakeWordController:
    def __init__(self):
        self._voice_assisstant_handler = None

    def check_word(self,text):
        words = text.lower().split(' ')
        for word in words:
            if word in WAKE_WORDS:
                print("I'm")
                self._voice_assisstant_handler.stop_engine()


    def load_assistant(self):
        self._voice_assisstant_handler = VoiceAssistantHandler(self.check_word)
        self._voice_assisstant_handler.run_engine()

    def stop_wake_word(self):
        self._voice_assisstant_handler.stop_engine()