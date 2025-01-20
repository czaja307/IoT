from .src import TerminalInteractions
from .src import TerminalCommunications
from common.mqqt_conf import STATUS_NOK, STATUS_OK
class TerminalApp:

    def __init__(self):
        self.communications = None
        self.interactions = None
        self.last_scanned_uid = None


    def quit_actions(self):
        print("Quitting app")
        self.communications.on_cleanup()
        quit()

    def process_rfid_card(self, uid):
        self.last_scanned_item = uid
        print(f"Scanned item: {uid}")
        self.communications.send_message(f"{uid}")

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
        self.interactions = TerminalInteractions()
        self.interactions.assign_quit_action(self.quit_actions)
        self.interactions.assign_card_read_action(self.process_rfid_card)

        self.communications = TerminalCommunications()
        self.communications.assign_response_action(self.server_response_received)
        self.communications.on_start()
        
        self.interactions.start_rfid_listener()

if __name__ == '__main__':
    app = TerminalApp()
    app.main()
    

