
class CheckoutLogic:

    def __init__(self):
        self._scanned_tags = []
        self._price = 0
        self._products = []
        self._current_index = 0

    def add_product(self, product):
        self._price += int(product["price"])
        self._products.append(product)

    def add_scanned_tag(self, tag) -> bool:
        if str(tag) in self._scanned_tags:
            return False
        self._scanned_tags.append(str(tag))
        return True
    
    def remove_last_scanned(self):
        if self._scanned_tags:
            self._scanned_tags = self._scanned_tags[:-1]

    def reset_session(self):
        self._price = 0
        self._scanned_tags = []
        self._products = []
        self._current_index = 0

    def get_tags(self):
        return self._scanned_tags

    def get_total(self):
        return self._price

    def remove_current_tag(self):
        if self._current_index > len(self._products) - 1:
            self._current_index = len(self._products) - 1
        elif self._current_index < 0:
            self._current_index = 0

        self._price -= int(self._products[self._current_index]["price"])
        self._products.pop(self._current_index)
        self._scanned_tags.pop(self._current_index)
        self._current_index -= 1
        if self._current_index >= len(self._products):
            self._current_index = max(0, len(self._products) - 1)

    def next_product(self):
        if self._current_index < len(self._products) - 1:
            self._current_index += 1

    def previous_product(self):
        if self._current_index > 0:
            self._current_index -= 1

    def get_current_product(self):
        return self._products[self._current_index]
