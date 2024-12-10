from abc import ABC, abstractmethod

class InteractionsInterface(ABC):
    def __init__(self):
        self._quit_action = None

    def assign_quit_action(self, action):
        self._quit_action = action

    def quit_sig_sent(self):
        self._quit_action()
