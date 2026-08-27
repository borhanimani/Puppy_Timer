# Puppy Timer - Design

## Design Goals

The design of Puppy Timer focuses on simplicity, clarity, and minimal interaction.   
   
Since the application is intended to be used during activities such as exercise, the interface should provide the necessary information without requiring the user to constantly interact with the application.
The main design goals are:

- Simple and easy-to-understand interaction
- Modern and clean visual design
- Clear presentation of timer information
- Minimal distractions during activities
- Clear feedback for user actions
- Easy access to the timer while using other applications


## Interface Design
The main interface was designed to provide the user with the information and controls needed to manage a timer without unnecessary complexity.
Visual elements and icons are used to make actions and system states easier to understand at a glance.
The interface follows a clean and modern visual style while keeping the number of visible controls focused on the application's primary purpose.


## Timer Interaction
The timer creation flow was designed around the idea that users typically create a timer for a specific activity and then use it.
For this reason, the current design does not provide a separate editing workflow for an existing timer. If the user wants to change the timer configuration, the existing timer can be removed and a new timer can be created.
This keeps the interaction simple and avoids introducing additional controls that are not essential to the primary use case.


## Exercise and Rest States
The timer clearly communicates the current stage of an activity.
The user can distinguish between active exercise and rest periods through the visual state of the interface and the timer information presented on screen.
This is intended to reduce the need for the user to constantly check or interact with the application while exercising.


## Voice Interaction
Voice interaction was designed to reduce the amount of physical interaction required while exercising.
The user can configure the desired exercise and rest durations through voice commands and start the timer when they are ready.
This allows the user to prepare for the exercise or work before the active timer begins, avoiding the loss of workout time that originally motivated the project.


## Mini Window
A small always-on-top window was introduced to make the timer easier to monitor while using other applications.
The purpose of the mini window is to provide the essential timer information without requiring the user to keep the main application window open and visible.
The window can be moved to a convenient position on the screen, allowing users to place it where it is least distracting while still keeping the timer visible.


## Design Process
The visual design process involved using Prompt engineering and prompt design, considering different UI/UX parameters and the needs.

##   
[< previous page](02_architecture.md)   &nbsp;&nbsp;&nbsp; [next page >](04_command_processing.md)
