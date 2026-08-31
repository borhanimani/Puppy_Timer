# Puppy Timer — User Guide

Puppy Timer provides two ways to manage timers:

1. **Manual Mode** — Create and manage a timer using the graphical interface.
2. **Puppy Assistant** — Create and manage a timer using voice commands.

> **Important:** Only one timer can exist at a time. To create a new timer, you must first delete the existing timer. This applies to both Manual Mode and Puppy Assistant.

---

# 1. Manual Mode

## Creating a Timer

To create a timer manually:

1. Open Puppy Timer and go to the main window.
2. Click the **Add (+)** button.
3. The timer settings page will open.
4. Set the desired **Focus Time**.
5. Set the desired **Rest Time**.
6. Click **Save**.

After saving, you will be returned to the main window.

The timer will display the total duration consisting of the focus and rest periods.

## Starting a Timer

Once a timer has been created, click the **Start** button to begin the timer.

## Deleting a Timer

To delete the current timer, click the **Trash** button.

After deleting the timer, you can create a new one using the **Add (+)** button.

> **Important:** You cannot create another timer while a timer already exists. Delete the current timer before creating a new one.

---

# 2. Puppy Assistant

Puppy Assistant allows you to create and control timers using voice commands.

## Activating the Assistant

Before using Puppy Assistant, you must first enable it from the **main window**.

1. Click the **Microphone** button.
2. Check your operating system for the microphone usage indicator.
3. When the microphone usage indicator appears, Puppy Assistant is ready to listen for the wake word.

The microphone must be enabled from the **main window** to prepare the assistant.

However, once the assistant has been prepared, you do **not** need to remain on the main window to activate Puppy Assistant with your voice.

---

## Activating Puppy with the Wake Word

Once the assistant is ready, say:

**"Puppy"**

or:

**"Hey Puppy"**

When Puppy detects the wake word, it will provide an audio response to indicate that it has been activated.

You will also see a visual indication on screen:

* In the **main window**, a green border will appear around the Puppy circle.
* In the **mini window**, a green screen with a green line at the bottom will indicate that Puppy is active and listening.

These indicators show that Puppy is ready to receive a command.

---

# 3. Creating a Timer with Puppy

To create a timer using Puppy Assistant, you must provide:

* The **total timer duration**
* The amount of **rest time**

For example:

> **"Set a timer for 1 minute and 15 seconds rest."**

Puppy will interpret this as:

* **Focus:** 45 seconds   
* **Rest:** 15 seconds

Therefore, the resulting timer will contain a total duration of **1 minute and 15 seconds**, consisting of **45 seconds of focus time followed by 15 seconds of rest**.

### Rest Time Is Optional

If you do not specify a rest duration, the entire requested duration will be used as focus time.

For example:

> **"Set a timer for 5 minutes."**

This creates:

* **Focus:** 5 minutes
* **Rest:** 0 minutes

However, if you provide **only the rest duration** without specifying the total timer duration, Puppy will not be able to understand the command.

For example:

> **"Set a timer for 15 seconds rest."**

is not sufficient because the total timer duration has not been specified.

> **Important:** Always provide the total timer duration. The rest duration can be omitted, but the total duration cannot.

---

# 4. Starting a Timer with Puppy

After creating a timer, you do not need to start it immediately.

Whenever you are ready to begin your focus session, rest session, workout, or any other activity you can use the timer for, simply activate Puppy and say one of the following commands:

* **"Start"**
* **"Run"**
* **"Go"**

For example, you can create a timer before starting a workout. When you are ready to begin the exercise, activate Puppy and say:

> **"Start."**

Puppy will start the current timer.

This allows you to prepare your timer in advance and start it whenever you are ready, without needing to return to the application window.

---

# 5. Deleting a Timer with Puppy

To delete the current timer, use one of the following commands:

* **"Delete"**
* **"Remove"**

For example:

> **"Delete."**

Puppy will remove the current timer.

After the timer has been deleted, you can create a new timer.

---

# 6. Timer Audio Notifications

Puppy Timer can provide audio notifications when different stages of the timer are completed.

If the required audio files have been added and configured according to the instructions provided in the project source code:

* When the **focus period** ends, Puppy Timer plays an audio notification indicating that the focus session has finished and the rest period is beginning.
* When the **rest period** ends, Puppy Timer plays another audio notification indicating that the entire timer has been completed.

The two notifications can use different sounds. The choice of sounds is up to you and can be configured according to the audio setup instructions provided in the source code.

> **Note:** Audio notifications depend on the corresponding audio files being added and configured correctly. They are not available unless the required audio resources have been set up according to the project's instructions.

---

# 7. After the Timer Finishes

When the timer reaches the end of its rest period, the entire timer session is complete.

The timer remains available after completion, so you can use the same timer again without creating a new one.

To start the same timer again, simply activate Puppy and say:

* **"Start"**
* **"Run"**
* **"Go"**

Alternatively, you can delete the completed timer and create a new one with different focus and rest durations.

To delete the current timer, use:

* **"Delete"**
* **"Remove"**

The same options are also available through the graphical interface using the **Start** and **Trash** buttons.

---

# 8. A Note from Puppy

Puppy is still in its first version, and its voice assistant may not always understand every command correctly.

If Puppy does not understand you the first time, please try saying the command again using a simple and clear phrase.

Thank you for your patience and understanding while Puppy continues to learn and improve. 

We hope Puppy makes your work sessions, breaks, workouts, and everyday activities a little more enjoyable.

---

# 9. Timer Management Summary

| Action          | Manual Mode    | Puppy Assistant          |
| --------------- | -------------- | ------------------------ |
| Create timer    | Add (+) button | Voice command            |
| Start timer     | Start button   | "Start", "Run", or "Go"  |
| Start again timer     | Start again button   | "Start", "Run", or "Go"  |
| Delete timer    | Trash button   | "Delete" or "Remove"     |
| Multiple timers | Not supported  | Not supported            |
| Rest duration   | Set manually   | Specify in voice command |
| Wake word       | Not required   | "Puppy" / "Hey Puppy"    |


---

## Important Notes

* Only **one timer** can exist at a time.
* Delete the existing timer before creating a new one.
* Puppy Assistant must first be enabled from the **main window**.
* After the assistant is prepared, the main window does not need to remain open for the wake word to activate Puppy.
* A timer command must include the **total duration**.
* Rest duration is optional. If omitted, the entire duration is treated as focus time.
* Puppy Assistant provides feedback when it successfully understands and executes a command.
