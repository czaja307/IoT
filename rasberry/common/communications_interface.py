from abc import ABC, abstractmethod
import socket

class CommunicationsInterface(ABC):

    def __init__(self):
        self._on_server_response = None

    @abstractmethod
    def send_message(self, message):
        pass

    def process_response(self, response):
        self._on_server_response(response)
    
    def get_ip_address(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    
    def assign_terminal_response_action(self, action):
        self._on_server_response = action