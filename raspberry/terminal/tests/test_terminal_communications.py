import pytest
from unittest.mock import MagicMock, Mock
from common.mqqt_conf import *
from ..src import TerminalCommunications



@pytest.fixture
def comms():
    comms = TerminalCommunications()
    comms.client = MagicMock()
    comms.get_ip_address = Mock(return_value="192.168.1.1")
    comms.client.connect = MagicMock()
    comms.client.subscribe = MagicMock()
    comms.client.publish = MagicMock()
    comms.client.loop_start = MagicMock()
    comms.client.loop_stop = MagicMock()
    comms.client.unsubscribe = MagicMock()
    yield comms
    

# Test Initialization
def test_initialization(comms):
    assert comms.broker == "10.10.10.10"
    assert comms.topic == ""

# Test send_message method
def test_send_message(comms):
    comms.topic = "test/topic"
    comms.send_message("Hello")
    comms.client.publish.assert_called_once_with("test/topic", "Hello")  #publish was called with correct args

# Test greeting_from_server method
def test_greeting_from_server(comms):
    mock_message = Mock()
    mock_message.payload.decode.return_value = "for#192.168.1.1#new_topic"
    
    # Call greeting_from_server
    comms.greeting_from_server(comms.client, None, mock_message)
    
    comms.client.unsubscribe.assert_called_once_with(GREETING_TOPIC)
    assert comms.topic == f"{TERMINAL_TOPIC}new_topic/"
    

# Test start_mosquitto method
def test_start_mosquitto(comms):
    

    # Call start_mosquitto
    comms.start_mosquitto()
    
    comms.client.connect.assert_called_once_with("10.10.10.10")
    comms.client.subscribe.assert_called_with(GREETING_TOPIC)
    comms.client.publish.assert_called_once_with(GREETING_TOPIC, "192.168.1.1")
    comms.client.loop_start.assert_called_once()

# Test stop_mosquitto method
def test_stop_mosquitto(comms):
   
    comms.topic = "test/topic"
    
    # Call stop_mosquitto
    comms.stop_mosquitto()
   
    comms.client.unsubscribe.assert_called_once_with("test/topic")
    comms.client.loop_stop.assert_called_once()
    comms.client.disconnect.assert_called_once()