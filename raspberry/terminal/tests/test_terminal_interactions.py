import pytest
from unittest.mock import MagicMock
from ..src import TerminalInteractions
try:
    import RPi.GPIO as GPIO
except:
    import Mock.GPIO as GPIO

# Test setup for TerminalInteractions
@pytest.fixture
def inters():
    inters = TerminalInteractions()
    yield inters 

@pytest.fixture
def inters_mocked():
    inters = TerminalInteractions()
    inters.setupButtons = MagicMock()
    inters.quit_sig_sent = MagicMock()
    yield inters

# Test for setupButtons method
def test_setup_buttons(inters, mocker):

    buttonRed = 5

    mock_add_event_detect = mocker.patch('Mock.GPIO.add_event_detect')

    inters.setupButtons()

    mock_add_event_detect.assert_called_once_with(
        buttonRed, 
        GPIO.FALLING, 
        callback=inters.redButtonPressed, 
        bouncetime=200
    )

# Test for quit_sig_sent method
def test_quit_signal_sent(inters, mocker):
    mock_cleanup = mocker.patch('Mock.GPIO.cleanup')
    inters.quit_sig_sent()
    mock_cleanup.assert_called_once()

# Test for redButtonPressed method (simulate button press for 1 second)
def test_red_button_pressed(inters_mocked, mocker):
    mock_time = mocker.patch('time.time', side_effect=[0, 1.1])  # Simulate 1.1 seconds passing
    mock_gpio_input = mocker.patch('Mock.GPIO.input', side_effect=[GPIO.LOW, GPIO.HIGH])  # Simulate button press/release
    # Simulate the red button being pressed
    inters_mocked.redButtonPressed(channel=5)

    inters_mocked.quit_sig_sent.assert_called_once()
    mock_gpio_input.assert_called()  # Ensure GPIO.input was called multiple times (for the button press and release)
    assert mock_gpio_input.call_count == 2

# Test for assign_quit_action method
def test_assign_quit_action(inters_mocked):
    mock_action = MagicMock()
    inters_mocked.assign_quit_action(mock_action)

    inters_mocked.setupButtons.assert_called_once()
    assert inters_mocked._quit_action == mock_action