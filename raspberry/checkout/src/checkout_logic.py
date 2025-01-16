
class CheckoutLogic:

    def __init__(self):
        self._scanned_tags = []
        self._price = 0

    def add_product(self, product):
        self._price += int(product["price"])

    def add_scanned_tag(self, tag) -> bool:
        if tag in self._scanned_tags:
            return False
        self._scanned_tags.append(str(tag))
        return True
    
    def remove_last_scanned(self):
        self._scanned_tags = self._scanned_tags[:-1]

    def reset_session(self):
        self._price = 0
        self._scanned_tags = []

    def get_tags(self):
        return self._scanned_tags

    def get_total(self):
        return self._price
