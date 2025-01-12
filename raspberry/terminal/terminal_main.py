from .src import TerminalInteractions
from .src import TerminalCommunications
import time
class TerminalApp:
    def quit_actions(self):
        print("Quitting app")
        self.communications.on_cleanup()
        quit()


    def main(self):
        print('Hello, World!')
        self.interactions = TerminalInteractions()
        self.interactions.assign_quit_action(self.quit_actions)
        self.communications = TerminalCommunications()
        self.communications.on_start()
        time.sleep(1)
        self.communications.send_message("3")
        while(True):
            time.sleep(1)
            pass

if __name__ == '__main__':
    app = TerminalApp()
    app.main()
    