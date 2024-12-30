from common.config import *
from common import InteractionsInterface
from common import RFIDInterface

try:
    import RPi.GPIO as GPIO
except:
    import Mock.GPIO as GPIO
import time

class TerminalInteractions(InteractionsInterface):

    def __init__(self):
        super().__init__()
        self.quitting = False
        self.rfid = RFIDInterface()
        

    def assign_quit_action(self, action):
        super().assign_quit_action(action)
        self.setupButtons()
        print("Quit assigned")

    def quit_sig_sent(self):
        self.quitting = True
        try:
            GPIO.cleanup()
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


    def start_rfid_listener(self, on_card_read_callback):
    	print("Starting RFID listener...")
		self.rfid.assign_card_read_callback(on_card_read_callback)
		try:
			while not self.quitting:
				uid = self.rfid.read_rfid()
				if uid:
					on_card_read_callback(uid)
				time.sleep(1)
		except KeyboardInterrupt:
			self.quit_sig_sent()