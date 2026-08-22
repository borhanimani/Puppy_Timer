from voice_assistant import VoiceEngine


def command(text):
    print(
        "heard:",
        text
    )


voice = VoiceEngine(
    "voice_assistant/models/vosk-model-small-en-us-0.15",
    command
)


try:

    voice.start()

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

    voice.stop()

    print(
        "Voice engine stopped"
    )