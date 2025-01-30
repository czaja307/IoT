from typing import List, Optional, Callable, Dict
from .mqtt_conf import *
import paho.mqtt.client as mqtt
from decorators import singleton


@singleton
class ServerCommunications:

    def __init__(self):
        self.client = mqtt.Client()
        self.broker = MQTT_BROKER
        self.subscribed_topics = [GREETING_TOPIC]
        self.registered_checkouts: List[int] = []
        self.registered_checkouts_count: int = 0
        self.registered_terminals: List[int] = []
        self.registered_terminals_count: int = 0
        self.on_checkout_msg: Optional[Callable] = None
        self.on_terminal_msg: Optional[Callable] = None
        self.terminals_products_dict: Dict[int, Optional[int]] = {}

    def on_start(self):
        self.start_mosquitto()

    def on_cleanup(self):
        self.stop_mosquitto()

    def send_message(self, topic, message):
        self.client.publish(topic, message)

    def remove_device(self, topic):
        segmented_topic = [ t for t in topic.split("/") if t]
        if len(segmented_topic) < 2:
            return
        id = int(segmented_topic[-1])
        if segmented_topic[0] in CHECKOUT_TOPIC:
            self.registered_checkouts.remove(id)
            self.registered_checkouts_count -= 1
            self.client.unsubscribe(f"{CHECKOUT_TOPIC}{id}/")
            self.subscribed_topics.remove(f"{CHECKOUT_TOPIC}{id}/")
        elif segmented_topic[0] in TERMINAL_TOPIC:
            self.registered_terminals.remove(id)
            self.registered_terminals_count -= 1
            self.client.unsubscribe(f"{TERMINAL_TOPIC}{id}/")
            self.subscribed_topics.remove(f"{TERMINAL_TOPIC}{id}/")
            if id in self.terminals_products_dict:
                del self.terminals_products_dict[id]

    def on_message(self, client, userdata, message):
        msg_topic = message.topic
        print(f"message on topic: {msg_topic}")
        message_decoded = str(message.payload.decode("utf-8"))
        if GREETING_TOPIC in msg_topic:
            self.greeting_from_raspberry(message_decoded)
        elif CHECKOUT_TOPIC in msg_topic:
            response = self.checkout_message(message_decoded)
            if response:
                self.send_message(f"{msg_topic}{RESPONSE_SUFFIX}", response)
        elif TERMINAL_TOPIC in msg_topic:
            response = self.terminal_message(message_decoded, msg_topic)
            if response:
                self.send_message(f"{msg_topic}{RESPONSE_SUFFIX}", response)
        elif FAREWELL_TOPIC in msg_topic:
            self.remove_device(message_decoded)


    def set_on_terminal_msg(self, func):
        self.on_terminal_msg = func

    def set_on_checkout_msg(self, func):
        self.on_checkout_msg = func

    def checkout_message(self, message):
        print(f"checkout: {message}")
        if self.on_checkout_msg:
            return self.on_checkout_msg(message)
        return None

    def terminal_message(self, message, topic):
        print(f"terminal: {message}")
        if self.on_terminal_msg:
            return self.on_terminal_msg(message, topic)
        return None

    def register_device(self, topic_type: str, ip: str, registered_count: int, registered_list: List[int]) -> None:
        topic = f"{topic_type}{registered_count}/"
        self.client.subscribe(topic)
        self.subscribed_topics.append(topic)
        self.send_message(f"{GREETING_TOPIC}{RESPONSE_SUFFIX}", f"for#{ip}#{registered_count}")
        registered_list.append(registered_count)

    def greeting_from_raspberry(self, message):
        parts = message.split("#")
        if len(parts) != 2:
            print("wrong message format")
            return

        if parts[0] == CHECKOUT_TOPIC:
            self.registered_checkouts_count += 1
            self.register_device(CHECKOUT_TOPIC, parts[1], self.registered_checkouts_count, self.registered_checkouts)
        elif parts[0] == TERMINAL_TOPIC:
            self.registered_terminals_count += 1
            self.register_device(TERMINAL_TOPIC, parts[1], self.registered_terminals_count, self.registered_terminals)
            self.terminals_products_dict[self.registered_terminals_count] = None
        else:
            print("incorrect topic")
            return

        print(f"registered successfully t: {self.registered_terminals}, c: {self.registered_checkouts}")

    def start_mosquitto(self):
        self.client.connect(self.broker)
        self.client.on_message = self.on_message
        self.client.loop_start()
        self.client.subscribe(GREETING_TOPIC)
        self.client.subscribe(FAREWELL_TOPIC)
        print("mosquitto started")

    def stop_mosquitto(self):
        for topic in self.subscribed_topics:
            self.client.unsubscribe(topic)
        self.client.loop_stop()
        self.client.disconnect()
        print("End of the show")
