import pytest
from unittest.mock import MagicMock
from ..src import TerminalInteractions  # Assuming this is saved in terminal_interactions.py

# Test setup for TerminalInteractions
@pytest.fixture
def terminal_interactions():
    return TerminalInteractions()

# Test for setupButtons method
def test_setup_buttons(terminal_interactions, mocker):

    buttonRed = 5
    mock_setmode = mocker.patch('RPi.GPIO.setmode')
    mock_setwarnings = mocker.patch('RPi.GPIO.setwarnings')
    mock_setup = mocker.patch('RPi.GPIO.setup')
    mock_add_event_detect = mocker.patch('RPi.GPIO.add_event_detect')

    terminal_interactions.setupButtons()

    mock_setmode.assert_called_once()
    mock_setwarnings.assert_called_once_with(False)
    mock_setup.assert_called()
    mock_add_event_detect.assert_called_once_with(
        buttonRed, 
        GPIO.FALLING, 
        callback=terminal_interactions.redButtonPressed, 
        bouncetime=200
    )

# Test for quit_sig_sent method
def test_quit_signal_sent(terminal_interactions, mocker):
    mock_cleanup = mocker.patch('RPi.GPIO.cleanup')

    terminal_interactions.quit_sig_sent()

    mock_cleanup.assert_called_once()

# Test for redButtonPressed method (simulate button press for 1 second)
def test_red_button_pressed(terminal_interactions, mocker):
    mock_time = mocker.patch('time.time', side_effect=[0, 1.1])  # Simulate 1.1 seconds passing
    mock_gpio_input = mocker.patch('RPi.GPIO.input', side_effect=[GPIO.LOW, GPIO.LOW, GPIO.HIGH])  # Simulate button press/release
    mock_quit_sig_sent = mocker.patch.object(terminal_interactions, 'quit_sig_sent')

    # Simulate the red button being pressed
    terminal_interactions.redButtonPressed(channel=5)

    mock_quit_sig_sent.assert_called_once()
    mock_gpio_input.assert_called()  # Ensure GPIO.input was called multiple times (for the button press and release)
    assert mock_gpio_input.call_count == 3

# Test for assign_quit_action method
def test_assign_quit_action(terminal_interactions, mocker):
    mock_action = MagicMock()

    # Mock the setupButtons method
    mocker.patch.object(terminal_interactions, 'setupButtons')

    terminal_interactions.assign_quit_action(mock_action)

    # Ensure that setupButtons was called
    terminal_interactions.setupButtons.assert_called_once()

    # Check if the quit action was set
    assert terminal_interactions.quit_action == mock_action