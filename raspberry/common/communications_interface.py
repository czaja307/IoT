from abc import ABC, abstractmethod
import netifaces

class CommunicationsInterface(ABC):

    def __init__(self):
        self._on_server_response = None

    @abstractmethod
    def send_message(self, message):
        pass

    @abstractmethod
    def on_start(self):
        pass

    @abstractmethod
    def on_cleanup(self):
        pass

    def process_response(self, response):
        self._on_server_response(response)
    
    def get_ip_address(self):
        interfaces = netifaces.interfaces()
        if 'eth0' in interfaces:
            eth0_info = netifaces.ifaddresses('eth0')
            return eth0_info[netifaces.AF_INET][0]['addr']
        return None
    
    def assign_response_action(self, action):
        self._on_server_response = action