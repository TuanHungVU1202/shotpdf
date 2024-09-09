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

    @patch('time.sleep')
    @patch('pyautogui.press')
    def test_simulate_valid_input(self, mock_press, mock_sleep):
        from service.input_simulator import simulate
        config = {'skey': 'a', 'delay_before': 1, 'delay_after': 2, 'repeat': 2}
        simulate(config)
        mock_sleep.assert_any_call(1)  # delay_before
        mock_sleep.assert_any_call(2)  # delay_after
        self.assertEqual(mock_press.call_count, 2)  # repeat
        mock_press.assert_called_with('a')

    @patch('logging.error')
    def test_simulate_missing_skey(self, mock_logging):
        from service.input_simulator import simulate
        simulate({})
        mock_logging.assert_called_with("No 'skey' found in the input object")

    @patch('logging.error')
    def test_simulate_invalid_input_type(self, mock_logging):
        from service.input_simulator import simulate
        simulate("not a dict")
        mock_logging.assert_called_with("Input is not a valid JSON-like object")

    @patch('time.sleep')
    @patch('pyautogui.press')
    def test_simulate_default_values(self, mock_press, mock_sleep):
        from service.input_simulator import simulate
        config = {'skey': 'b'}
        simulate(config)
        mock_sleep.assert_any_call(0)  # default delay_before
        mock_sleep.assert_any_call(0)  # default delay_after
        mock_press.assert_called_with('b')
        self.assertEqual(mock_press.call_count, 1)  # default repeat is 1


if __name__ == '__main__':
    unittest.main()