import pytest
from unittest import mock
from common import CommunicationsInterface
from common.mqqt_conf import *
import paho.mqtt.client as mqtt
from ..src import TerminalCommunications # Adjust based on your import paths

# Mocking the MQTT Client
@pytest.fixture
def mock_mqtt_client():
    # Mock the MQTT client object
    mock_client = mock.Mock(mqtt.Client)
    return mock_client

# Test Initialization
def test_initialization(mock_mqtt_client):
    comm = TerminalCommunications()
    assert comm.client is mock_mqtt_client
    assert comm.broker is None
    assert comm.topic == ""

# Test send_message method
def test_send_message(mock_mqtt_client):
    comm = TerminalCommunications()
    comm.client = mock_mqtt_client  # Assign the mock client
    comm.topic = "test/topic"
    
    comm.send_message("Hello")
    
    comm.client.publish.assert_called_once_with("test/topic", "Hello")  # Ensure publish was called with correct args

# Test greeting_from_server method
def test_greeting_from_server(mock_mqtt_client):
    comm = TerminalCommunications()
    comm.client = mock_mqtt_client  # Assign the mock client
    comm.broker = "broker_address"
    
    # Mock the get_ip_address method
    comm.get_ip_address = mock.Mock(return_value="192.168.1.1")
    
    # Define a mock message object
    mock_message = mock.Mock()
    mock_message.payload.decode.return_value = "for#192.168.1.1#new_topic"
    
    # Call greeting_from_server
    comm.greeting_from_server(mock_mqtt_client, None, mock_message)
    
    # Check if unsubscribe was called
    comm.client.unsubscribe.assert_called_once_with(GREETING_TOPIC)
    
    # Check if topic was updated
    assert comm.topic == f"{TERMINAL_TOPIC}new_topic/"
    
    # Check that subscribe was called with the new topic
    comm.client.subscribe.assert_called_once_with(f"{TERMINAL_TOPIC}new_topic/")

# Test start_mosquitto method
def test_start_mosquitto(mock_mqtt_client):
    comm = TerminalCommunications()
    comm.client = mock_mqtt_client  # Use the mock client
    comm.broker = "broker_address"
    
    # Mock the get_ip_address method
    comm.get_ip_address = mock.Mock(return_value="192.168.1.1")
    
    # Call start_mosquitto
    comm.start_mosquitto()
    
    # Check if the client connects
    comm.client.connect.assert_called_once_with("broker_address")
    
    # Check if subscribe was called for GREETING_TOPIC
    comm.client.subscribe.assert_called_with(GREETING_TOPIC)
    
    # Check if the correct message was published
    comm.client.publish.assert_called_once_with(GREETING_TOPIC, "192.168.1.1")
    
    # Ensure loop_start is called
    comm.client.loop_start.assert_called_once()

# Test stop_mosquitto method
def test_stop_mosquitto(mock_mqtt_client):
    comm = TerminalCommunications()
    comm.client = mock_mqtt_client  # Use the mock client
    comm.topic = "test/topic"
    
    # Call stop_mosquitto
    comm.stop_mosquitton()
    
    # Check that the client unsubscribes from the topic
    comm.client.unsubscribe.assert_called_once_with("test/topic")
    
    # Ensure loop_stop is called
    comm.client.loop_stop.assert_called_once()
    
    # Ensure disconnect is called
    comm.client.disconnect.assert_called_once()