from common.config import *
from common import InteractionsInterface
from common import RFIDInterface

try:
    import RPi.GPIO as GPIO
except:
    import Mock.GPIO as GPIO
import time
import board
import neopixel

class TerminalInteractions(InteractionsInterface):

    def __init__(self):
        super().__init__()
        self.quitting = False
        self.rfid = RFIDInterface()
        self.pixels = neopixel.NeoPixel(board.D18, 8, brightness=0.3, auto_write=False)
        

    def assign_quit_action(self, action):
        super().assign_quit_action(action)
        self.setupButtons()
        print("Quit assigned")

    def quit_sig_sent(self):
        self.quitting = True
        try:
            self.cleanup()
            self.rfid_reader.cleanup()
            super().quit_sig_sent()
        except Exception as e:
            print(f"Exception occurred in quit_sig_sent: {e}")
         

    def redButtonPressed(self, channel):
        start_time = time.time()
        while not self.quitting and GPIO.input(channel) == GPIO.LOW:
            if time.time() - start_time >= 1:
                self.quit_sig_sent()
                

    def setupButtons(self):
        GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=self.redButtonPressed, bouncetime=200)


    def buzzer(self, state):
        GPIO.output(buzzerPin, not state)

    def run_buzzer(self):
        self.buzzer(True)

    def stop_buzzer(self):
        self.buzzer(False)

    def set_pixels_color(self, color):
        self.pixels.fill(color)
        self.pixels.show()

    def indicate_success(self):
        self.set_pixels_color((0, 255, 0))
        self.run_buzzer()
        time.sleep(0.5)
        self.pixels.fill((0, 0, 0))
        self.stop_buzzer()

    def indicate_error(self):
        self.set_pixels_color((255, 0, 0))
        time.sleep(0.5)
        self.pixels.fill((0, 0, 0))

    def cleanup(self):
        self.set_pixels_color((0, 0, 0)) 
        GPIO.cleanup()

    def start_rfid_listener(self):
        print("Starting RFID listener...")
        try:
            while not self.quitting:
                uid = self.rfid.read_rfid()
                if uid:
                    self.indicate_success()
                else:
                    self.indicate_error()
                time.sleep(0.3)
        except KeyboardInterrupt:
            self.quit_sig_sent()