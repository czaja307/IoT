
from .mqtt_conf import *
import paho.mqtt.client as mqtt

class ServerCommunications:

    def __init__(self):
        self.client = mqtt.Client()
        self.broker = MQTT_BROKER
        self.subscribed_topics = [GREETING_TOPIC]
        self.registered_checkouts = 0 
        self.registered_terminals = 0 
        self.on_checkout_msg = None
        self.on_terminal_msg = None

    def on_start(self):
        self.start_mosquitto()

    def on_cleanup(self):
        self.stop_mosquitto()

    def send_message(self, topic, message):
        self.client.publish(topic, message)

    def on_message(self, client, userdata, message):
        msg_topic = message.topic
        print(f"message on topic: {msg_topic}")
        message_decoded = str(message.payload.decode("utf-8"))
        if GREETING_TOPIC in msg_topic:
            self.greeting_from_raspberry(message_decoded)
        elif CHECKOUT_TOPIC in msg_topic:
            response = self.checkout_message(message_decoded)
            self.send_message(f"{msg_topic}resp/", response)
        elif TERMINAL_TOPIC in msg_topic:
            response = self.terminal_message(message_decoded, msg_topic)
            self.send_message(f"{msg_topic}resp/", response)

    def set_on_terminal_msg(self, func):
        self.on_terminal_msg = func

    def set_on_checkout_msg(self, func):
        self.on_checkout_msg = func

    def checkout_message(self, message):
        print(f"checkout: {message}")
        if self.on_checkout_msg:
            return self.on_checkout_msg(message)
        return None

    def terminal_message(self, message):
        print(f"terminal: {message}")
        if self.on_terminal_msg:
            return self.on_terminal_msg(message, topic)
        return None

    def register_device(self, topic_type: str, ip: str, registered_count: int, registered_list: List[int]) -> None:
        topic = f"{topic_type}{registered_count}/"

        self.client.subscribe(topic)
        self.subscribed_topics.append(topic)
        self.send_message(GREETING_TOPIC, f"for#{ip}#{registered_count}")
        registered_list.append(registered_count)

    def greeting_from_raspberry(self, message):
        parts = message.split("#")
        if len(parts) == 2:
            print("message received")
            if parts[0] == CHECKOUT_TOPIC:
                self.registered_checkouts += 1
                self.client.subscribe(f"{CHECKOUT_TOPIC}{self.registered_checkouts}/")
                self.subscribed_topics.append(f"{CHECKOUT_TOPIC}{self.registered_checkouts}/")
                self.send_message(GREETING_TOPIC, f"for#{parts[1]}#{self.registered_checkouts}")
            elif parts[0] == TERMINAL_TOPIC:
                self.registered_terminals += 1
                self.client.subscribe(f"{TERMINAL_TOPIC}{self.registered_terminals}/")
                self.subscribed_topics.append(f"{TERMINAL_TOPIC}{self.registered_terminals}/")
                self.send_message(GREETING_TOPIC, f"for#{parts[1]}#{self.registered_terminals}")
            print(f"registered t: {self.registered_terminals}, c: {self.registered_checkouts}")
            

    def start_mosquitto(self):
        self.client.connect(self.broker)
        self.client.on_message = self.on_message
        self.client.loop_start()
        self.client.subscribe(GREETING_TOPIC)
        print("mosquitto started")

    def stop_mosquitto(self):
        for topic in self.subscribed_topics:
            self.client.unsubscribe(topic)
        self.client.loop_stop()
        self.client.disconnect()
        print("End of the show")


    