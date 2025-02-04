from .src import CheckoutInteractions
from .src import CheckoutCommunications
from .src import CheckoutLogic
import ast
import time
from common.mqqt_conf import STATUS_NOK

class CheckoutApp:

    def __init__(self):
        self.last_scanned_item = None
        self.communications = None
        self.interactions = None
        self.logic = None
        """State 1 means that an actual current state is checkout"""
        self.state = 0

    def quit_actions(self):
        print("Quitting app")
        self.logic.reset_session()
        self.interactions.display_manager.display_message("Wyłączono.")
        self.communications.on_cleanup()
        quit()

    def server_response_received(self, response):
        if self.logic.get_tags() != []:
            if response == STATUS_NOK:
                self.logic.remove_last_scanned()
                print("Could not scan the tag")
                self.interactions.display_manager.display_message("Nie istnieje")
                self.interactions.indicate_error()
                return
            product = ast.literal_eval(response)
            print(f"Product assigned to tag (id={product['id']}):\nname: {product['name']}\ndesc: {product['description']}\nprice: {product['price']}")
            self.logic.add_product(product)
            self.interactions.display_product_details(self.logic.get_id(), product['name'], product['price'])
            self.interactions.indicate_success()
        else:
            if response == STATUS_NOK:
                print("Checkout failed")
                self.interactions.indicate_error()

    def start_checkout(self):
        self.state = 0
        self.interactions.display_manager.display_message("Zacznij skanowanie.")
        
    def finish_checkout(self):
        self.interactions.checking_out = True
        tags = self.logic.get_tags()
        if len(tags) == 0:
            print("Cannot checkout an empty cart. Scan an item first.")
            self.interactions.display_manager.display_message("Pusty koszyk.")
            return
        total = self.logic.get_total()
        print(f"The total price for your shopping is: {total}.")
        self.interactions.display_total_price(total)
        tags_string = "#".join(tags)
        self.communications.send_message(f"BUY#{tags_string}")
        self.state = 0
        self.logic.reset_session()
        time.sleep(1)
        self.start_checkout()
        self.interactions.checking_out = False

    def cancel_checkout(self):
        print("Your shopping was cancelled.")
        self.interactions.display_cancel_message()
        self.logic.reset_session()
        self.state = 0
        self.start_checkout()

    def process_rfid_card(self, uid):
        # self.last_scanned_item = uid
        if self.state == 1:
            return
        if self.logic.add_scanned_tag(uid):
            print(f"Scanned item: {uid}")
            self.communications.send_message(f"{uid}")
            self.interactions.buzz()
        else:
            print("Item already scanned")
            self.interactions.buzz()
            self.interactions.indicate_error()

    def cancel_action(self):
        if self.state == 0:
            self.cancel_checkout()
        else:
            if self.logic.is_cart_empty():
                self.cancel_checkout()
            else:
                self.logic.remove_current_tag()
                self.interactions.display_manager.display_message("Usunięto.")

    def confirm_action(self):
        print("Zielone i jazda")
        if self.state == 1:
            self.finish_checkout()
            self.state = 0
        else:
            self.state = 1
            self.interactions.display_checkout_message()


    def next(self):
        if self.state == 1:
            print("BBB")
            self.logic.next_product()
            self.interactions.display_product_details(self.logic.get_id(), self.logic.get_current_product()['name'], self.logic.get_current_product()['price'])

    def prev(self):
        if self.state == 1:
            print("AAAA")
            self.logic.previous_product()
            self.interactions.display_product_details(self.logic.get_id(), self.logic.get_current_product()['name'], self.logic.get_current_product()['price'])
        
    def main(self):
        self.interactions = CheckoutInteractions()
        self.communications = CheckoutCommunications()
        self.logic = CheckoutLogic()

        self.interactions.assign_confirm_action(self.confirm_action)
        self.interactions.assign_cancel_action(self.cancel_action)
        self.interactions.assign_quit_action(self.quit_actions)
        self.interactions.assign_card_read_action(self.process_rfid_card)
        self.interactions.assign_next_action(self.next)
        self.interactions.assign_prev_action(self.prev)

        self.communications.assign_response_action(self.server_response_received)
        self.communications.on_start()

        self.start_checkout()
        self.interactions.start_rfid_listener()


if __name__ == '__main__':
    app = CheckoutApp()
    app.main()
