from common import CommunicationsInterface
from common.mqqt_conf import *
import paho.mqtt.client as mqtt

class TerminalCommunications(CommunicationsInterface):

    def __init__(self):
        super().__init__()
        self.client = mqtt.Client()
        self.broker = MQTT_BROKER
        self.topic = "."
        
    def send_message(self, message):
        self.client.publish(self.topic, message)

    def on_start(self):
        super().on_start()
        self.start_mosquitto()

    def on_cleanup(self):
        super().on_cleanup()
        self.stop_mosquitto()

    def on_message(self, client, userdata, message):
        message_decoded = (str(message.payload.decode("utf-8")))
        print(message_decoded)
        self.process_response(message_decoded)

    def greeting_from_server(self, client, userdata, message):
        message_decoded = (str(message.payload.decode("utf-8")))
        parts = message_decoded.split("#")
        if len(parts) == 3 and parts[0] == "for":
            if self.get_ip_address() == parts[1]:
                self.client.unsubscribe(GREETING_TOPIC)
                self.topic = f"{TERMINAL_TOPIC}{parts[2]}/"
                self.client.on_message = self.on_message
                self.client.subscribe(f"{self.topic}resp/")
                print("Treminal is ready to send messages.")

    def start_mosquitto(self):
        self.client.on_message = self.greeting_from_server
        self.client.will_set(FAREWELL_TOPIC, self.topic)
        self.client.connect(self.broker)
        self.client.loop_start()
        self.client.subscribe(GREETING_TOPIC)
        self.client.publish(GREETING_TOPIC, f"{TERMINAL_TOPIC}#{self.get_ip_address()}")
        print("mosquitto ")

    def stop_mosquitto(self):
        self.client.unsubscribe(self.topic)
        self.client.loop_stop()
        self.client.disconnect()


    