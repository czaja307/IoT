from common.config import *
from common import InteractionsInterface
try:
    import RPi.GPIO as GPIO
except:
    import Mock.GPIO as GPIO
import time

class TerminalInteractions(InteractionsInterface):

    def __init__(self):
        super().__init__()
        self.quitting = False
        

    def assign_quit_action(self, action):
        super().assign_quit_action(action)
        self.setupButtons()
        print("Quit assigned")

    def quit_sig_sent(self):
        self.quitting = True
        try:
            GPIO.cleanup()
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