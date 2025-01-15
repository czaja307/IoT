from .src import TerminalInteractions
from .src import TerminalCommunications
import time
from common.mqqt_conf import STATUS_NOK, STATUS_OK
class TerminalApp:
    def __init__(self):
        self.communications = None
        self.interactions = None

    def quit_actions(self):
        print("Quitting app")
        self.communications.on_cleanup()
        quit()


    def server_response_received(self, response):
        if response == STATUS_OK:
            print("Product assigned to the scanned tag!")
            self.interactions.indicate_success()
        elif response == STATUS_NOK:
            print("Could not assign product to the scanned tag!")
            self.interactions.indicate_error()
        else:
            print("Invalid response from server!")

    def main(self):
        print('Hello, World!')
        self.interactions = TerminalInteractions()
        self.interactions.assign_quit_action(self.quit_actions)
        self.communications = TerminalCommunications()
        self.communications.assign_response_action(self.server_response_received)
        self.communications.on_start()

if __name__ == '__main__':
    app = TerminalApp()
    app.main()
    