from common.SSD1331 import SSD1331
from common.display_manager import DisplayManager

if __name__ == '__main__':
    display = SSD1331()
    manager = DisplayManager(display)
    # manager.display_message("Cancelled")
    # manager.display_product_details("Banany", 15)
    manager.display_total_price(150)