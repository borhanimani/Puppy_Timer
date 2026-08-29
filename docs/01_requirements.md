# Puppy Timer - Requirements 

## Description:    
The requirements of the application are:  

### Functional Requirements   
Puppy Timer should provide the core functionality required to manage time-based activities and workouts.

- The system should allow users to create timer.
- The system should support separate exercise and rest intervals.
- Users should be able to specify how long the active and rest periods should last.
- The system should provide voice-based control for timer operations.
- Users should be able to give voice commands to configure and control timer.
- The system should recognize when the user is ready to begin and allow the timer to start through a voice command.
- The system should clearly indicate the current state of the timer, such as exercise or rest.
- The system should provide appropriate notifications when an interval changes or a timer finishes.


### User Requirements
The application should provide both traditional manual controls and voice-based interaction so that users can choose the interaction method that best fits their situation.

- Users should be able to manage timer using the graphical interface.
- Users should be able to manage timers using voice commands.
- Users should be able to specify the duration of exercise and rest periods.
- Users should be able to prepare for an activity before starting the timer.
- Users should be able to start the timer without needing to interact physically with the application.
- Users should be able to understand the current timer state without unnecessary interaction.
- Users sould be able to use voice assistant manually.


### UI/UX Requirements
The interface should be simple, lightweight, modern, and easy to understand.

- The application should provide a clean and modern interface.
- Timer information should be presented clearly and be easy to understand at a glance.
- The current activity state should be clearly visible, such as exercise or rest.
- The interface should provide visual feedback when a voice command is received or processed.
- Users should be able to understand whether the system is listening, processing a command, or has completed an action.
- Transitions between exercise and rest periods should be clearly communicated.
- The application should include a small, always-on-top window for keeping the timer visible while using other applications. (mini-window)
- The mini window should be movable so that users can place it wherever it is most convenient on the screen.
- Common timer operations should require minimal interaction.
- The michrophone button for running voice processing action.


### Security & Privacy Requirements
Privacy should be considered as part of the voice-based functionality.

- Voice processing should be performed locally whenever possible.
- User audio should not be transmitted to external servers for the core voice functionality.
- The application should not permanently store users' voice recordings.
- The core functionality of the application should not require an internet connection.
- The use of local voice processing should reduce the application's dependence on external services.
- The voice processing action will not begin until the user run in manually by cicking on michrophone.


### Performance Requirements
The application should remain lightweight and responsive during normal operation.

- The application should have low resource consumption.
- Voice processing should not block or freeze the graphical user interface.
- Timer operations should remain responsive while other components are running.
- The application should start and respond quickly during normal use.
- The application should be lightweight enough to run on a wide range of hardware.
- Background processes should be managed efficiently to avoid unnecessary resource usage.


### Offline Capability
Puppy Timer should be designed to provide its core functionality without depending on an internet connection.

- The timer system should work completely offline.
- Voice recognition should be performed locally using an offline speech-recognition system.
- Internet access should not be required for normal timer operation.
- The application should not depend on continuous communication with cloud-based services.


### Maintainability & Extensibility
The application should have a modular structure that makes it easier to maintain, improve, and extend.

- Major components should have clearly defined responsibilities.
- Independent systems should be separated from one another where appropriate.
- Components should be reusable where possible.
- Changes to one component should have minimal impact on unrelated components.
- The architecture should allow new features to be added without requiring major changes to existing systems.
- The codebase should remain understandable and maintainable as the project grows.
- The system should provide a foundation for potentially adapting the application to different hardware or resource-constrained environments.


##   
[< previous page](00_motivation.md)   &nbsp;&nbsp;&nbsp; [next page >](02_architecture.md)
