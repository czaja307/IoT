from abc import ABC, abstractmethod

class InteractionsInterface(ABC):
    def __init__(self):
        self._quit_action = None

    def assign_quit_action(self, action):
        self._quit_action = action

    def quit_sig_sent(self):
        print("U STAREGO")
        if self._quit_action:
            try:
                self._quit_action()
            except Exception as e:
                print(f"Exception in _quit_action: {e}")
        else:
            print("No quit action assigned.")