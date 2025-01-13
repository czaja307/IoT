from .src import CheckoutInteractions
from .src import CheckoutCommunications
import time

class CheckoutApp:

    def __init__(self):
        self.last_scanned_item = None
        self.communications = None
        self.interactions = None

    def quit_actions(self):
        print("Quitting app")
        self.communications.on_cleanup()
        quit()

    def server_response_received(self, response):
        pass

    def finish_checkout(self):
        pass

    def cancel_checkout(self):
        pass

    def process_rfid_card(self, uid):
        self.last_scanned_item = uid
        print(f"Scanned item: {uid}")
        self.communications.send_message(f"checkout#{uid}")

    def main(self):
        self.interactions = CheckoutInteractions()
        self.interactions.assign_confirm_action(self.finish_checkout)
        self.interactions.assign_cancel_action(self.cancel_checkout)
        self.interactions.assign_quit_action(self.quit_actions)

        self.communications = CheckoutCommunications()
        self.communications.assign_response_action(self.server_response_received)
        self.communications.on_start()
        time.sleep(1)
        self.communications.send_message("3")

        self.interactions.start_rfid_listener()


if __name__ == '__main__':
    app = CheckoutApp()
    app.main()