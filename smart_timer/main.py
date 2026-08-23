from voice_assistant.handler import VoiceAssistantHandler
from controller.timer_voice_contoller import TimerVoiceController
from controller.wake_word_controller import WakeWordController

# def command(text):
#     print(
#         "heard:",
#         text
#     )

# handler = VoiceAssistantHandler(command)
# handler.run_engine()

# a = TimerVoiceController()
# a.load_assistant()

b = WakeWordController()
b.load_assistant()