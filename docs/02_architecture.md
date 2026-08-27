# Puppy Timer - Architecture

## Architecture Overview   

Puppy Timer is built around two main systems: the Timer System and the Voice Assistant System.
The Timer System is responsible for timer-related functionality and is divided into two main components: the Timer UI and the Timer Controller.
The Voice Assistant System is responsible for capturing and processing voice input and converting speech into text. The Timer Controller then processes the resulting text and converts it into commands that can be understood and executed by the timer system.
The main components are designed to remain as independent and loosely coupled as possible. This separation makes the system easier to maintain, reuse, test, and extend, while also making it possible to replace or adapt individual components without requiring major changes to the rest of the application.

## Main Components

### Timer System

The Timer System is responsible for managing the timer and providing the user interface required to interact with it.
It consists of two main parts:
- **Timer UI** — responsible for presenting timer information and allowing the user to interact with the timer.
- **Timer Controller** — responsible for timer logic, state management, and timer operations.
The current version of Puppy Timer intentionally focuses on managing one timer at a time. The user creates a timer, uses it, and can remove it when it is no longer needed before creating another one.
This decision was made to keep the interaction simple and focused on the primary use case of the application rather than introducing the additional complexity of managing multiple timers simultaneously.

### Voice Assistant System
The Voice Assistant System is responsible for handling voice input and converting it into text.
The voice system is designed as a set of independent components rather than a single monolithic module. Microphone management, voice processing, wake word detection, and voice activity detection are separated so that individual components can be maintained or replaced independently.
This structure also makes it possible to use different libraries or implementations for specific parts of the voice pipeline without requiring major changes to the rest of the system.
The Voice Assistant does not directly control the timer. Instead, it provides processed text to the Timer Controller, keeping voice processing separate from application-specific command processing.

### Command Processing

After the Voice Assistant converts the user's speech into text, the text needs to be interpreted before the timer can use it.
The Timer Controller uses a custom command-processing algorithm that analyzes the recognized text, identifies the intended timer operation, extracts relevant values such as work and rest durations, and converts them into structured commands that the timer can understand and execute.
Keeping command processing separate from speech recognition allows the command-processing system to potentially receive text from other input sources in the future. This part of the project was also an opportunity to apply concepts I had previously learned about algorithm design to a practical problem.
   
The design and processing flow of this algorithm are described in more detail in [Command Processing](04_command_processing.md).

### Keyword Configuration
The voice command processing system uses a separate keyword configuration file to define the words and phrases that can be recognized as commands, time units, numbers, and other relevant inputs.
Keeping these keywords outside of the main command-processing logic makes the system easier to maintain and update without changing the core algorithm.
This structure also makes it easier to support additional languages in the future. Instead of changing the command-processing algorithm for each language, language-specific keywords can be added or organized separately while keeping the main processing logic unchanged.

## Modularity and Separation of Concerns
The main systems are designed with separation of concerns in mind. Each component is responsible for a specific part of the application and exposes only the functionality required by other components.
The Voice Assistant focuses on voice input and speech processing, while the Timer Controller focuses on interpreting commands and managing timer-related operations. The UI is responsible for presenting information and handling user interaction.
This separation reduces coupling between components and makes individual modules easier to reuse in other projects.
For example, the voice-processing system can potentially be used independently in another application that requires offline speech recognition, while the command-processing logic can receive text from a different input source without requiring changes to the timer itself.


## Offline Architecture
Puppy Timer is designed to operate without an internet connection.
The voice-processing pipeline runs locally instead of relying on cloud-based speech recognition services. This reduces the application's dependency on external services and allows the application to remain functional in environments where internet access is unavailable.
Local processing also supports the goal of keeping user audio within the device rather than sending it to external servers.


## Privacy and Resource Management
The application does not permanently store the user's voice recordings as part of its normal voice-processing workflow.
Avoiding unnecessary audio storage serves two purposes. First, it reduces the amount of user data retained by the application and therefore improves privacy. Second, it avoids unnecessary storage and processing requirements, supporting the goal of keeping the application lightweight.
The voice system processes audio locally and uses temporary data during processing rather than maintaining a permanent collection of user recordings.


## Wake Word
A wake word mechanism is used to control when the system should actively listen for timer commands.
The wake word acts as an entry point into the voice interaction flow. Once the wake word is detected, the system can focus on processing the user's following command.
This approach reduces unnecessary command processing and provides a more controlled interaction model for the voice assistant.


## Threading and Audio Queuing
Voice processing runs separately from the graphical user interface so that audio capture and processing do not block the UI thread.
Separating these operations allows the interface to remain responsive while the voice system is listening and processing audio.
An audio queue is also used between audio capture and processing. This provides a buffer between the microphone input and the speech-processing system. Since audio can be captured continuously while processing may take a different amount of time, the queue helps manage this difference and reduces the risk of losing or incorrectly processing incoming audio data.
The separation of these operations also makes the individual systems easier to control and shut down safely.

##    
