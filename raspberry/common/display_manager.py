from config import *
from SSD1331 import SSD1331
from PIL import Image, ImageDraw, ImageFont

class DisplayManager:
    def __init__(self, display):
        self.display = display
        self.display.Init()
        self.display.clear()

        try:
            self.font_large = ImageFont.truetype('/raspberry/common/Font.ttf', 20)
            self.font_small = ImageFont.truetype('/raspberry/common/Font.ttf', 15)
        except IOError:
            raise Exception("Nie znaleziono pliku czcionki 'Font.ttf'")

    def display_product_details(self, name, price):
        image = Image.new("RGB", (self.display.width, self.display.height), "BLACK")
        draw = ImageDraw.Draw(image)

        draw.text((5, 5), f"Product: {name}", font=self.font_small, fill="WHITE")
        draw.text((5, 25), f"Price: {price:.2f} PLN", font=self.font_small, fill="WHITE")

        self.display.ShowImage(image, 0, 0)

    def display_total_price(self, totalPrice):
        image = Image.new("RGB", (self.display.width, self.display.height), "BLACK")
        draw = ImageDraw.Draw(image)

        draw.text((5, 15), f"Total: {totalPrice:.2f} PLN", font=self.font_large, fill="WHITE")

        self.display.ShowImage(image, 0, 0)

    def display_clear(self):
        self.display.clear()