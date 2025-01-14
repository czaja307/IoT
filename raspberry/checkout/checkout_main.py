from .src import CheckoutInteractions
from .src import CheckoutCommunications
import time
import ast

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
        product = ast.literal_eval(response)
        print(f"Product assigned to tag (id={product[id]}):\nname: {product["name"]}\ndesc: {product["description"]}\nprice: {product["price"]}")

    def finish_checkout(self):
        pass

    def cancel_checkout(self):
        pass

    def main(self):
        print('Hello, World!')
        self.interactions = CheckoutInteractions()
        self.interactions.assign_confirm_action(self.finish_checkout)
        self.interactions.assign_cancel_action(self.cancel_checkout)
        self.interactions.assign_quit_action(self.quit_actions)
        self.interactions.assign_card_read_action(self.process_rfid_card)

        self.communications = CheckoutCommunications()
        self.communications.assign_response_action(self.server_response_received)
        self.communications.on_start()
        time.sleep(1)
        self.communications.send_message("3")
        while True:
            time.sleep(1)


if __name__ == '__main__':
    app = CheckoutApp()
    app.main()