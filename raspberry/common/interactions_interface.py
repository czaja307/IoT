from abc import ABC, abstractmethod

class InteractionsInterface(ABC):
    def __init__(self):
        self._quit_action = None
        self._confirm_action = None
        self._cancel_action = None
        self._card_read_action = None

    def assign_quit_action(self, action):
        self._quit_action = action

    def assign_confirm_action(self, action):
        self._confirm_action = action

    def assign_cancel_action(self, action):
        self._cancel_action = action

    def assign_card_read_action(self, action):
        self.on_card_read = action

    def card_read(self, data):
        if self._card_read_action:
            try:
                self._card_read_action(data)
            except Exception as e:
                print(f"Exception in card_read_action: {e}")
        else:
            print("No card read action assigned.")

    def quit_sig_sent(self):
        if self._quit_action:
            try:
                self._quit_action()
            except Exception as e:
                print(f"Exception in quit_action: {e}")
        else:
            print("No quit action assigned.")

    def confirm_sig_sent(self):
        if self._confirm_action:
            try:
                self._confirm_action()
            except Exception as e:
                print(f"Exception in confirm_action: {e}")
        else:
            print("No confirm action assigned.")

    def cancel_sig_sent(self):
        if self._cancel_action:
            try:
                self._cancel_action()
            except Exception as e:
                print(f"Exception in cancel_action: {e}")
        else:
            print("No cancel action assigned.")