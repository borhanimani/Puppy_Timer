from voice_assistant.handler import VoiceAssistantHandler
from controller.timer_controller import TimerController


# def command(text):
#     print(
#         "heard:",
#         text
#     )

# handler = VoiceAssistantHandler(command)
# handler.run_engine()



class timerVoiceController:

    def __init__(self, timer_controller = TimerController):
        self._timer_controller = timer_controller
        self._voice_handler = None

    def get_command(self):
        self._voice_handler = VoiceAssistantHandler(None)
        self._voice_handler.run_engine

