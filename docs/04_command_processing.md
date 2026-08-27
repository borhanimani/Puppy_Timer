# Puppy Timer - Command Processing

## Overview
Puppy Timer uses a custom text-processing algorithm to convert recognized voice commands into instructions that the timer can understand.
The algorithm processes the input text word by word and looks for four main types of information: the requested command, a number, a time unit, and the time mode. These values are then used to determine the appropriate timer operation.
The keywords used by the algorithm are kept in a separate configuration file, making it easier to update the supported commands and add support for other languages in the future.

## Algorithm

```text
INPUT: recognized text

1. Convert the text to lowercase and split it into words.

2. For each word:
   
   a. Check if the word represents a command.
      - Create -> "set"
      - Start  -> "start"
      - Delete -> "delete"

   b. Check if the word represents a number.
      - Also check the current word together with the next word
        to support multi-word numbers.

   c. Check if the word represents a time unit.
      - Minutes -> "min"
      - Seconds -> "sec"

   d. Check if the word represents a time mode.
      - Work/total time -> "total"
      - Rest time -> "rest"

3. If the command is "start":
      Start the timer and stop processing.

4. If the command is "delete":
      Delete the timer and stop processing.

5. If a number, time unit, and time mode have been identified:
      Convert the time to seconds if necessary.

      If the mode is "total":
          store the value as total time.

      If the mode is "rest":
          store the value as rest time.

6. After processing the text:

   If a valid timer command was identified:
      Send the total time and rest time to the timer system.

   Otherwise:
      Report that the command could not be processed.
```   

## Complexity
The command-processing algorithm has a time complexity of **O(n)**, where `n` is the number of words in the input text.
Each word is processed once, while the keyword and number lookups use dictionary operations with an average time complexity of **O(1)**.
The space complexity is **O(n)** because the input text is split into a list of words before processing.


##   
