from .src import TerminalInteractions
from .src import TerminalCommunications

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


if __name__ == '__main__':
    app = TerminalApp()
    app.main()