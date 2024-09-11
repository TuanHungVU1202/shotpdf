import tempfile
import unittest
from unittest.mock import patch, MagicMock
import os
from PIL import Image
from service.screenshooter import generate_default_screenshot_name, generate_default_screenshot_path, take_screenshot, save_screenshot

class TestScreenshooter(unittest.TestCase):

    @patch('service.screenshooter.pyautogui.screenshot')
    def test_take_screenshot_success(self, mock_screenshot):
        # Test successful screenshot capture
        mock_image = MagicMock(spec=Image.Image)
        mock_screenshot.return_value = mock_image
        
        result = take_screenshot()
        
        self.assertEqual(result, mock_image)
        mock_screenshot.assert_called_once()
        del mock_image


    @patch('service.screenshooter.pyautogui.screenshot')
    def test_take_screenshot_failure(self, mock_screenshot):
        # Test screenshot capture failure
        mock_screenshot.side_effect = Exception("Screenshot failed")
        
        result = take_screenshot()
        
        self.assertIsNone(result)


    @patch('service.screenshooter.datetime')
    def test_generate_default_screenshot_name(self, mock_datetime):
        # Test generate_default_screenshot_name
        mock_now = MagicMock()
        mock_now.strftime.return_value = "20230101_120000"
        mock_datetime.now.return_value = mock_now

        result = generate_default_screenshot_name()

        self.assertEqual(result, "screenshot_20230101_120000.png")
        mock_datetime.now.assert_called_once()
        mock_now.strftime.assert_called_once_with("%Y%m%d_%H%M%S")


    @patch('service.screenshooter.os.getcwd')
    @patch('service.screenshooter.generate_default_screenshot_name')
    def test_generate_default_screenshot_path(self, mock_generate_name, mock_getcwd):
        # Test generate_default_screenshot_path
        mock_getcwd.return_value = "/home/user"
        mock_generate_name.return_value = "screenshot_20230101_120000.png"

        result = generate_default_screenshot_path()

        self.assertEqual(result, "/home/user/screenshot_20230101_120000.png")
        mock_getcwd.assert_called_once()
        mock_generate_name.assert_called_once()


    @patch('service.screenshooter.generate_default_screenshot_path')
    def test_save_screenshot_default_path(self, mock_generate_path):
        # Test save_screenshot with default path
        mock_screenshot = MagicMock(spec=Image.Image)
        expected_path = "/home/user/screenshot_20230101_120000.png"
        mock_generate_path.return_value = expected_path

        result = save_screenshot(mock_screenshot)

        self.assertEqual(result, expected_path)
        mock_screenshot.save.assert_called_once_with(expected_path)
        mock_generate_path.assert_called_once()


    @patch('service.screenshooter.os.path.isdir')
    @patch('service.screenshooter.generate_default_screenshot_name')
    def test_save_screenshot_custom_directory(self, mock_generate_name, mock_isdir):
        # Test save_screenshot with custom directory
        mock_screenshot = MagicMock(spec=Image.Image)
        mock_isdir.return_value = True
        expected_image_name = "screenshot_20230101_120000.png"
        mock_generate_name.return_value = expected_image_name
        
        with tempfile.TemporaryDirectory() as custom_dir:
            result = save_screenshot(mock_screenshot, custom_dir)

        expected_path = os.path.join(custom_dir, expected_image_name)
        self.assertEqual(result, expected_path)
        mock_screenshot.save.assert_called_once_with(expected_path)
        mock_generate_name.assert_called_once()


    def test_save_screenshot_custom_path(self):
        # Test save_screenshot with custom path
        mock_screenshot = MagicMock(spec=Image.Image)

        # Create a temporary file with a .png extension
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            custom_path = temp_file.name

        self.addCleanup(os.remove, custom_path)

        result = save_screenshot(mock_screenshot, custom_path)
        self.assertEqual(result, custom_path)
        mock_screenshot.save.assert_called_once_with(custom_path)


    @patch('service.screenshooter.os.makedirs')
    @patch('service.screenshooter.os.path.exists')
    def test_save_screenshot_create_directory(self, mock_exists, mock_makedirs):
        # Test save_screenshot creates directory if it doesn't exist
        mock_screenshot = MagicMock(spec=Image.Image)
        custom_path = "/new/directory"
        final_save_path = os.path.join(custom_path, generate_default_screenshot_name())
        mock_exists.return_value = False

        result = save_screenshot(mock_screenshot, custom_path)

        mock_screenshot.save.assert_called_once_with(final_save_path)
        self.assertEqual(result, final_save_path)


    def test_save_screenshot_failure(self):
        # Test save_screenshot failure
        mock_screenshot = MagicMock(spec=Image.Image)
        mock_screenshot.save.side_effect = Exception("Save failed")

        result = save_screenshot(mock_screenshot)

        self.assertIsNone(result)
        mock_screenshot.save.assert_called_once()


if __name__ == '__main__':
    unittest.main()