from common.config import *
from common import InteractionsInterface
from common import RFIDInterface
from common.SSD1331 import SSD1331
from common.display_manager import DisplayManager
from paho.mqtt.subscribe import callback

from common.config import encoderLeft, encoderRight

try:
    import RPi.GPIO as GPIO
except:
    import Mock.GPIO as GPIO
import time
import board
import neopixel

class CheckoutInteractions(InteractionsInterface):

    def __init__(self):
        super().__init__()

        self.quitting = False
        self.was_red_released = True
        self.was_green_released = True
        self.rfid = RFIDInterface()
        self.pixels = neopixel.NeoPixel(board.D18, 8, brightness=0.3, auto_write=False)

        display = SSD1331()
        self.display_manager = DisplayManager(display)

        self.on_next = None
        self.on_prev = None

        self.encoder_left_previous_state = GPIO.input(encoderLeft)
        self.encoder_right_previous_state = GPIO.input(encoderRight)

    def assign_next_action(self, action):
        self.on_next = action

    def assign_prev_action(self, action):
        self.on_prev = action
        
    def assign_quit_action(self, action):
        super().assign_quit_action(action)
        self.setupButtons()
        self.setup_encoder()
        print("Quit assigned")

    def quit_sig_sent(self):
        self.quitting = True
        try:
            self.cleanup()
            super().quit_sig_sent()
        except Exception as e:
            print(f"Exception occurred in quit_sig_sent: {e}")

    def display_product_details(self, num, name, price):
        self.display_manager.display_product_details(num, name, price)

    def display_total_price(self, totalPrice):
        self.display_manager.display_total_price(totalPrice)

    def display_cancel_message(self):
        self.display_manager.display_message("Cancelled")

    def display_checkout_message(self):
        # I'm not sure if the whole thing will fit on the small display
        self.display_manager.display_message("SUMMARY", "encoder-scroll.")

    def redButtonPressed(self, channel):
        start_time = time.time()
        while not self.quitting and GPIO.input(channel) == GPIO.LOW:
            if time.time() - start_time >= 1:
                self.quit_sig_sent()
        
        if not self.quitting and GPIO.input(channel) == GPIO.HIGH:
            self.cancel_sig_sent()

    def greenButtonPressed(self, channel):
        self.confirm_sig_sent()

       
    def setupButtons(self):
        GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=self.redButtonPressed, bouncetime=1000)
        GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=self.greenButtonPressed, bouncetime=1000)

    def buzzer(self, state):
        GPIO.output(buzzerPin, not state)

    def run_buzzer(self):
        self.buzzer(True)

    def stop_buzzer(self):
        self.buzzer(False)

    def buzz(self):
        self.run_buzzer()
        time.sleep(0.5)
        self.stop_buzzer()

    def set_pixels_color(self, color):
        self.pixels.fill(color)
        self.pixels.show()

    def setup_encoder(self):
        GPIO.add_event_detect(encoderLeft, GPIO.FALLING, callback=self.handle_encoder, bouncetime=50)
        GPIO.add_event_detect(encoderRight, GPIO.FALLING, callback=self.handle_encoder, bouncetime=50)

    def handle_encoder(self, channel):
        encoder_left_current_state = GPIO.input(encoderLeft)
        encoder_right_current_state = GPIO.input(encoderRight)

        if (self.encoder_left_previous_state == 1 and encoder_left_current_state == 0):
            print("Encoder Right")
            if self.on_next:
                self.on_next()
        elif (self.encoder_right_previous_state == 1 and encoder_right_current_state == 0):
            print("Encoder Left")
            if self.on_prev:
                self.on_prev()

        self.encoder_left_previous_state = encoder_left_current_state
        self.encoder_right_previous_state = encoder_right_current_state

    def indicate_success(self):
        self.set_pixels_color((0, 255, 0))
        time.sleep(0.5)
        self.set_pixels_color((0, 0, 0))

    def indicate_error(self):
        self.set_pixels_color((255, 0, 0))
        time.sleep(0.5)
        self.set_pixels_color((0, 0, 0))

    def cleanup(self):
        self.set_pixels_color((0, 0, 0)) 
        GPIO.cleanup()

    def start_rfid_listener(self):
        print("Starting RFID listener...")
        try:
            while not self.quitting:
                uid = self.rfid.read_rfid()
                if uid:
                    self.card_read(uid)
                time.sleep(0.3)
        except KeyboardInterrupt:
            self.quit_sig_sent()




