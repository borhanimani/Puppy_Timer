from voice_assistant.handler import VoiceAssistantHandler

def command(text):
    print(
        "heard:",
        text
    )

handler = VoiceAssistantHandler(command)
handler.run_engine()

