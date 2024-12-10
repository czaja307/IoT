from common import CommunicationsInterface
from common.mqqt_conf import *
import paho.mqtt.client as mqtt

class TerminalCommunications(CommunicationsInterface):

    def __init__(self):
        super().__init__()
        self.client = mqtt.Client()
        self.broker = None
        self.topic = ""

    def send_message(self, message):
        self.client.publish(self.topic, message)


    def greeting_from_server(self, client, userdata, message):
        message_decoded = (str(message.payload.decode("utf-8")))
        parts = message_decoded.split("#")
        if len(parts) == 3 and parts[0] == "for":
            if self.get_ip_address() == parts[1]:
                self.client.unsubscribe(GREETING_TOPIC)
                self.topic = f"{TERMINAL_TOPIC}{parts[2]}/"
                self.client.on_message = None
                self.client.subscribe(self.topic)


    def start_mosquitto(self):
        self.client.connect(self.broker)
        self.client.on_message = self.greeting_from_server
        self.client.loop_start()
        self.client.subscribe(GREETING_TOPIC)
        self.client.publish(GREETING_TOPIC, self.get_ip_address())

    def stop_mosquitton(self):
        self.client.unsubscribe(self.topic)
        self.client.loop_stop()
        self.client.disconnect()


    