from . import config
from . import SSD1331
from PIL import Image, ImageDraw, ImageFont

class DisplayManager:
    def __init__(self, display):
        self.display = display
        self.display.Init()
        self.display.clear()

        try:
            self.font_small = ImageFont.truetype('./common/Font.ttf', 10)
            self.font_large = ImageFont.truetype('./common/Font.ttf', 15)
        except IOError:
            raise Exception("Nie znaleziono pliku czcionki 'Font.ttf'")

    def display_product_details(self, name, price):
        image = Image.new("RGB", (self.display.width, self.display.height), "BLACK")
        draw = ImageDraw.Draw(image)

        draw.text((5, 5), f"Produkt: {name}", font=self.font_small, fill="WHITE")
        draw.text((5, 25), f"Cena: {price:.2f} PLN", font=self.font_small, fill="WHITE")

        self.display.ShowImage(image, 0, 0)

    def display_total_price(self, totalPrice):
        image = Image.new("RGB", (self.display.width, self.display.height), "BLACK")
        draw = ImageDraw.Draw(image)

        draw.text((5, 15), f"Suma: {totalPrice:.2f} PLN", font=self.font_small, fill="WHITE")

        self.display.ShowImage(image, 0, 0)

    def display_message(self, message):
        image = Image.new("RGB", (self.display.width, self.display.height), "BLACK")
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), f"{message}", font=self.font_large, fill="WHITE")

        self.display.ShowImage(image, 0, 0)

    def display_clear(self):
        self.display.clear()