import RPI.GPIO
from mfrc522 import MFR522

class RFIDInterface:
	def __init__(self):
		self.reader = MFRC522()
		self._on_card_read = None


	@staticmethod
	def uid_to_int(uid):
		return sum(byte << (i * 8) for i, byte in enumerate(uid))
		

	def assign_card_read_callback(self, callback):
        self._on_card_read = callback


	def read_rfid(self):
		(status, tag_type) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
		if status == self.reader.MI_OK:
			(status, uid) = self.reader.MFRC522_Anticoll()
			if status == self.reader.MI_OK:
				uid_int = self.uid_to_int(uid)
				print(f"RFID card detected: UID={uid}")
				return uid_int
			else:
				print("RFID card read failed")
		else:
			print("No RFID card detected")
		return None

	def cleanup(self):
		GPIO.cleanup()