import RPI.GPIO
from mfrc522 import MFR522

class RFIDInterface:
	def __init__(self):
		self.reader = MFRC522()

	def read_rfid(self):
		(status, tag_type) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
		if status == self.reader.MI_OK:
			(status, uid) = self.reader.MFRC522_Anticoll()
			if status == self.reader.MI_OK:
				print(f"RFID card detected: UID={uid}")
				return uid
			else:
				print("RFID card read failed")
		else:
			print("No RFID card detected")
		return None

	def cleanup(self):
		GPIO.cleanup()