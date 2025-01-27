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
        self.state = 0 # State 1 means that an actual current state is checkout

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
                self.interactions.indicate_error()
                return
            product = ast.literal_eval(response)
            print(f"Product assigned to tag (id={product['id']}):\nname: {product['name']}\ndesc: {product['description']}\nprice: {product['price']}")
            self.interactions.display_product_details(product['name'], product['price'])
            self.logic.add_product(product)
            self.interactions.indicate_success()
        else:
            if response == STATUS_NOK:
                print("Checkout failed")
                self.interactions.indicate_error()
                self.logic.remove_last_scanned()
        
    def finish_checkout(self):
        tags = self.logic.get_tags()
        if len(tags) == 0:
            print("Cannot checkout an empty cart. Scan an item first.")
            return
        total = self.logic.get_total()
        print(f"The total price for your shopping is: {total}.")
        self.interactions.display_total_price(total)
        tags_string = "#".join(tags)
        self.communications.send_message(f"BUY#{tags_string}")
        self.logic.reset_session()

    def cancel_checkout(self):
        print("Your shopping was cancelled.")
        self.interactions.display_cancel_message()
        self.logic.reset_session()

    def process_rfid_card(self, uid):
        self.last_scanned_item = uid
        if self.logic.add_scanned_tag(uid):
            print(f"Scanned item: {uid}")
            self.communications.send_message(f"{uid}")
            self.interactions.buzz()
        else:
            print("Item already scanned")
            self.interactions.buzz()
            self.interactions.indicate_error()

    def cancel_action(self):
        if self.state == 1:
            return self.cancel_checkout
        else:
            return self.logic.remove_current_tag

    def confirm_action(self):
        if self.state == 1:
            return self.finish_checkout
        else:
            def change_state():
                self.state = 1
            return change_state

    def next(self):
        self.logic.next_product()
        self.interactions.display_product_details(self.logic.get_current_product())

    def prev(self):
        self.logic.previous_product()
        self.interactions.display_product_details(self.logic.get_current_product())
        
    def main(self):
        self.interactions = CheckoutInteractions()
        self.communications = CheckoutCommunications()
        self.logic = CheckoutLogic()

        self.interactions.assign_confirm_action(self.confirm_action)
        self.interactions.assign_cancel_action(self.cancel_action)
        self.interactions.assign_quit_action(self.quit_actions)
        self.interactions.assign_card_read_action(self.process_rfid_card)
        self.interactions.assign_next_action(self.next)
        self.interactions.assign_next_action(self.prev)

        self.communications.assign_response_action(self.server_response_received)
        self.communications.on_start()

        self.interactions.start_rfid_listener()


if __name__ == '__main__':
    app = CheckoutApp()
    app.main()