from .src import CheckoutInteractions
from .src import CheckoutCommunications
from .src import CheckoutLogic
import ast
import time

class CheckoutApp:

    def __init__(self):
        self.last_scanned_item = None
        self.communications = None
        self.interactions = None
        self.logic = None

    def quit_actions(self):
        print("Quitting app")
        self.logic.reset_session()
        self.communications.on_cleanup()
        quit()

    def server_response_received(self, response):
        product = ast.literal_eval(response)
        print(f"Product assigned to tag (id={product["id"]}):\nname: {product["name"]}\ndesc: {product["description"]}\nprice: {product["price"]}")
        self.logic.add_product(product)
        
    def finish_checkout(self):
        tags = self.logic.get_tags()
        if len(tags) == 0:
            print("Cannot checkout an empty cart. Scan an item first.")
            return
        total = self.logic.get_total()
        print(f"The total price for your shopping is: {total}.")
        tags_string = "#".join(tags)
        self.communications.send_message(f"BUY#{tags_string}")
        self.logic.reset_session()

    def cancel_checkout(self):
        print("Your shopping was cancelled.")
        self.logic.reset_session()

    def main(self):
        print('Hello, World!')
        self.interactions = CheckoutInteractions()
        self.communications = CheckoutCommunications()
        self.logic = CheckoutLogic()

        self.interactions.assign_confirm_action(self.finish_checkout)
        self.interactions.assign_cancel_action(self.cancel_checkout)
        self.interactions.assign_quit_action(self.quit_actions)
        self.interactions.assign_card_read_action(self.process_rfid_card)

        self.communications.assign_response_action(self.server_response_received)
        self.communications.on_start()

        #testing starts here
        input("Press enter to scan item 3")
        self.communications.send_message("3")
        input("Press enter to scan item 1")
        self.communications.send_message("1")
        self.finish_checkout()


if __name__ == '__main__':
    app = CheckoutApp()
    app.main()