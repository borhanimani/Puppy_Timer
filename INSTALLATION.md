## Installation  

### Requirements:
  Before running Puppy Timer, make sure you have:    
  - Python version 3.x  
  - A working microphone for using voice features

### Setup Instructions:   
  1. Clone the project: 
    https://github.com/borhanimani/Smart_Timer.git   
    *you can download the project zip and extract it*
    
  2. Open the project file or go to the project file with the command:   
     ```cd smart_timer```

  3. Setting up the Virtual Environment:
     #### Windows:  
       ```python -m venv myenv```
     
     #### macOS / Linux:  
       ```python3 -m venv myenv```

  4. Activating the Virtual Environment:
     #### Windows:
       ```myenv\Scripts\activate```  

     #### macOS / Linux:
       ```source myenv/bin/activate```    
       *after activating you will see something similar to: (myenv)*

  5. Installing Required Packeges:   
       ```pip install -r requirements.txt```

  6. downloading Vosk model:
     *download your vosk model, I used "vosk-model-small-en-us-0.15"*.
     Place the model inside:
       ```voice_assistant/models/```

  7. Run the program:   
       ```python main.py```
