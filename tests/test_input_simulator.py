import unittest
from unittest.mock import patch
from service.input_simulator import input_simulator_health, simulate_page_up_down

class TestInputSimulator(unittest.TestCase):

    def test_input_simulator_health(self):
        # Capture the printed output
        with patch('builtins.print') as mock_print:
            input_simulator_health()
            mock_print.assert_called_with("Input Simulator Health Check")

    @patch('time.sleep')
    @patch('pyautogui.press')
    def test_simulate_page_up_down(self, mock_press, mock_sleep):
        simulate_page_up_down()
        
        # Check if sleep was called with correct arguments
        mock_sleep.assert_any_call(5)
        mock_sleep.assert_any_call(1)
        
        # Check if press was called with correct arguments
        mock_press.assert_any_call('pagedown')
        mock_press.assert_any_call('pagedup')

if __name__ == '__main__':
    unittest.main()