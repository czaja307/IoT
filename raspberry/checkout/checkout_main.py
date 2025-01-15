from .src import CheckoutInteractions
from .src import CheckoutCommunications
from .src import CheckoutLogic
import ast
from common.mqqt_conf import STATUS_NOK

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
        if self.logic.get_tags() != []:
            if response == STATUS_NOK:
                self.logic.remove_last_scanned()
                print("Could not scan the tag")
                return
            product = ast.literal_eval(response)
            print(f"Product assigned to tag (id={product['id']}):\nname: {product['name']}\ndesc: {product['description']}\nprice: {product['price']}")
            self.logic.add_product(product)
        else:
            if response == STATUS_NOK:
                print("Checkout failed")
        
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

    def process_rfid_card(self, uid):
        self.last_scanned_item = uid
        if self.logic.add_scanned_tag(uid):
            print(f"Scanned item: {uid}")
            self.communications.send_message(f"{uid}")
            self.interactions.indicate_success()
        else:
            print("Item already scanned")
            self.interactions.indicate_error()
        
    def main(self):
        self.interactions = CheckoutInteractions()
        self.communications = CheckoutCommunications()
        self.logic = CheckoutLogic()

        self.interactions.assign_confirm_action(self.finish_checkout)
        self.interactions.assign_cancel_action(self.cancel_checkout)
        self.interactions.assign_quit_action(self.quit_actions)

        self.communications.assign_response_action(self.server_response_received)
        self.communications.on_start()

        self.interactions.start_rfid_listener()


if __name__ == '__main__':
    app = CheckoutApp()
    app.main()