import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
from PIL import Image
from service.pdf_handler import get_images_sorted_by_modification, save_images_to_pdf, append_images_to_pdf

class TestPDFHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        # Create 3 images with different extensions
        cls.create_test_image('image1.png', 500)
        cls.create_test_image('image2.jpg', 900)
        cls.create_test_image('image3.bmp', 3000)
        # Create a text file
        cls.create_test_text_file('not_an_image.txt', 800)

    @classmethod
    def tearDownClass(cls):
        for file in os.listdir(cls.temp_dir):
            os.remove(os.path.join(cls.temp_dir, file))
        os.rmdir(cls.temp_dir)

    @classmethod
    def create_test_image(cls, filename, modified_time):
        path = os.path.join(cls.temp_dir, filename)
        with Image.new('RGB', (100, 100), color='red') as img:
            img.save(path)
        os.utime(path, (modified_time, modified_time))

    @classmethod
    def create_test_text_file(cls, filename, modified_time):
        path = os.path.join(cls.temp_dir, filename)
        with open(path, 'w') as f:
            f.write('This is not an image')
        os.utime(path, (modified_time, modified_time))

    def test_get_images_sorted_by_modification(self):
        result = get_images_sorted_by_modification(self.temp_dir)

        expected = [
            os.path.join(self.temp_dir, 'image1.png'),
            os.path.join(self.temp_dir, 'image2.jpg'),
            os.path.join(self.temp_dir, 'image3.bmp')
        ]
        self.assertEqual(result, expected)

    @patch('service.pdf_handler.canvas.Canvas')
    def test_save_images_to_pdf(self, mock_canvas):
        mock_canvas_instance = MagicMock()
        mock_canvas.return_value = mock_canvas_instance

        output_pdf = os.path.join(self.temp_dir, 'output.pdf')
        result = save_images_to_pdf(self.temp_dir, output_pdf)

        self.assertEqual(result, output_pdf)
        mock_canvas.assert_called_once_with(output_pdf)
        self.assertEqual(mock_canvas_instance.drawImage.call_count, 3)
        mock_canvas_instance.save.assert_called_once()

    def test_save_images_to_pdf_no_images(self):
        # Create a new empty directory for this test
        empty_dir = tempfile.mkdtemp()
        output_pdf = os.path.join(empty_dir, 'output.pdf')
        result = save_images_to_pdf(empty_dir, output_pdf)

        self.assertIsNone(result)
        self.assertFalse(os.path.exists(output_pdf))
        os.rmdir(empty_dir)

    @patch('service.pdf_handler.canvas.Canvas')
    def test_append_images_to_pdf(self, mock_canvas):
        mock_canvas_instance = MagicMock()
        mock_canvas.return_value = mock_canvas_instance

        existing_pdf = os.path.join(self.temp_dir, 'existing.pdf')
        open(existing_pdf, 'w').close()  # Create an empty file

        result = append_images_to_pdf(self.temp_dir, existing_pdf)

        self.assertEqual(result, existing_pdf)
        mock_canvas.assert_called_once_with(existing_pdf)
        self.assertEqual(mock_canvas_instance.drawImage.call_count, 3)
        mock_canvas_instance.save.assert_called_once()

    def test_append_images_to_pdf_no_images(self):
        # Create a new empty directory for this test
        empty_dir = tempfile.mkdtemp()
        existing_pdf = os.path.join(empty_dir, 'existing.pdf')
        open(existing_pdf, 'w').close()  # Create an empty file

        result = append_images_to_pdf(empty_dir, existing_pdf)

        self.assertEqual(result, existing_pdf)
        os.remove(existing_pdf)
        os.rmdir(empty_dir)

if __name__ == '__main__':
    unittest.main()