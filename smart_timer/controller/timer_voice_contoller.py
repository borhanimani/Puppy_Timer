from voice_assistant.handler import VoiceAssistantHandler
from controller.timer_controller import TimerController
from controller.keywords import *


class TimerVoiceController:
    _Assistant_called = False

    def __init__(self, timer_controller = TimerController):
        self._timer_controller = timer_controller
        self._voice_handler = None

    def get_number(self, word1, word2):
        if word1 in NUMBERS_EN:
            if word2 in NUMBERS_EN:
                return NUMBERS_EN[(word1+' '+word2)]
            
            else:
                return NUMBERS_EN[word1]

        else:    
            return None


    def get_time_unit(self, word):
        if word in TIME_UNIT_MINITUE_EN:
            return 'min'

        if word in TIME_UNIT_SECOND_EN:
            return 'sec'

        return None

    def get_command(self, word):
        if word in COMMAND_CREATE_EN:
            return 'set'

        if word in COMMAND_START_EN:
            return 'start'

        return None

    def get_time_mode(self, word):
        if word in TIME_WORK_MODE_EN:
            return 'total'

        if word in TIME_REST_MODE_EN:
            return 'rest'

        return None

    def time_in_second(self, time, unit):
        if unit == 'min':
            return time * 60

        return time 

    def get_text(self, text):
        print(text)

        words = text.lower().split(' ')
        # self._Assistant_called = self.check_wake_word(words)

        # if not self._Assistant_called:
            # return 

        print("CHECKING >>>>>")

        total_time_second = 0
        rest_time_second = 0
        command = ''
        number= -1
        time_unit = ''
        time_mode = ''
        command_identified = False
        number_identified = False
        time_unit_identified = False
        time_mode_identifed = False

        for i in range(len(words)):
            word = words[i]

            command = self.get_command(word)
            if command != None:
                command_identified = True

            number = self.get_number(word,words[i+1])
            if number != -1:
                number_identified = True

            time_unit = self.get_time_unit(word)
            if time_unit != None:
                time_unit_identified = True

            time_mode = self.get_time_mode(word)
            if time_mode != None:
                time_mode_identifed = True

            if command_identified:
                command_identified = False
                if command == "start":
                    return
                    # call an func
    
                if (number_identified and time_unit_identified and time_mode_identifed):
                    number_identified = False
                    time_unit_identified = False
                    time_mode_identifed = False

                    if time_mode == 'total':
                        total_time_second = self.time_in_second(number, time_unit)

                    if time_mode == 'rest':
                        rest_time_second = self.time_in_second(number, time_unit)

        print('total: ',total_time_second)
        print('rest: ',rest_time_second)



    def load_assistant(self):
        self._voice_handler = VoiceAssistantHandler(self.get_text)
        self._voice_handler.run_engine()

    def stop_assistant(self):
        self._voice_handler.stop_engine()
        print("Assistant Stoped.")


