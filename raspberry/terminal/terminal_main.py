from .src import TerminalInteractions
from .src import TerminalCommunications
import time
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
        self.communications.send_message(f"terminal#{uid}")

    def main(self):
        print('Hello, World!')
        self.interactions = TerminalInteractions()
        self.interactions.assign_quit_action(self.quit_actions)
        
        self.communications = TerminalCommunications()
        self.communications.on_start()
        
        self.interactions.start_rfid_listener(self.process_rfid_card)

if __name__ == '__main__':
    app = TerminalApp()
    app.main()
    

