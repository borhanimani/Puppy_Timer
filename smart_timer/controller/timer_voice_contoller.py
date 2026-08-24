from PySide6.QtCore import QObject, Signal
from voice_assistant.handler import VoiceAssistantHandler
from controller.keywords import *

class TimerVoiceController(QObject):
    createTimerSignal = Signal(int, int)
    startTimerSignal = Signal()
    deleteTimerSignal = Signal()

    voiceStartedSignal = Signal()
    voiceFailedSignal = Signal()
    voiceSuccessSignal = Signal()

    _Assistant_called = False

    def __init__(self, ui_handler):

        super().__init__()

        self._voice_handler = None
        self._ui_handler = ui_handler 


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

        if word in COMMAND_DELETE_EN:
            return 'delete'

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
        print('text: ',text)

        words = text.lower().split(' ')
        print("CHECKING >>>>>")

        total_time_second = 0
        rest_time_second = 0
        word = ''
        word2 = ''
        command = ''
        number= None
        time_unit = ''
        time_mode = ''
        command_identified = False
        number_identified = False
        time_unit_identified = False
        time_mode_identifed = False
        command_is_real = False

        for i in range(len(words)):
            word = words[i]
            if (i+1) < len(words):
                word2 = words[i+1]

            # print('===============================')

            if not command_identified:
                command = self.get_command(word)

            # print('command: ', command)

            if command != None:
                command_identified = True


            if not number_identified:
                number = self.get_number(word,word2)

            # print('number: ', number)

            if number != None:
                number_identified = True

            if not time_unit_identified:
                time_unit = self.get_time_unit(word)

            # print('time unit: ', time_unit)

            if time_unit != None:
                time_unit_identified = True


            if not time_mode_identifed:
                time_mode = self.get_time_mode(word)

            # print('time mode: ', time_mode)

            if time_mode != None:
                time_mode_identifed = True

            if command == "start":
                command_identified = False
                self.startTimerSignal.emit()
                return

            if command == 'delete':
                command_identified = False
                self.deleteTimerSignal.emit()
                return

            if (number_identified and time_unit_identified and time_mode_identifed):
                command_identified = False
                number_identified = False
                time_unit_identified = False
                time_mode_identifed = False
                command_is_real = True

                if time_mode == 'total':
                    total_time_second = self.time_in_second(number, time_unit)

                if time_mode == 'rest':
                    rest_time_second = self.time_in_second(number, time_unit)

        if command_is_real:
            # self._ui_handler.create_ui_timer(total_time_second,rest_time_second)
            self.voiceSuccessSignal.emit()
            self.createTimerSignal.emit(
                total_time_second,
                rest_time_second
            )
            print('===============================')
            print('total: ',total_time_second)
            print('rest: ',rest_time_second)
            print('===============================')

        else:
            self.voiceFailedSignal.emit()

    def load_assistant(self):
        if self._voice_handler:
            return

        self._voice_handler = VoiceAssistantHandler(self.get_text)
        self._voice_handler.start()

    def stop_assistant(self):
        if self._voice_handler:
            self._voice_handler.stop()
            self._voice_handler = None
            print("Assistant Stoped.")


