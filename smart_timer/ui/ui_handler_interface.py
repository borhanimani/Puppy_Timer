from abc import ABC, abstractmethod


class UiHandlerInterface(ABC):

    @abstractmethod
    def create_ui_timer(self, total, rest):
        pass

    @abstractmethod
    def start_ui_timer(self):
        pass