from voice_assistant.handler import VoiceAssistantHandler


def on_text(text):

    print("HEARD:", text)


assistant = VoiceAssistantHandler(on_text)

assistant.start()

print("Voice assistant started.")
print("Press Ctrl+C to stop.")

try:

    while True:
        pass

except KeyboardInterrupt:

    print("Stopping...")

finally:

    assistant.stop()

    print("Stopped.")