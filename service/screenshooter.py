import pyautogui # type: ignore
import os
from PIL import Image
from datetime import datetime

def take_screenshot() -> Image.Image:
    """
    Take a full screen screenshot.

    Returns:
    Image.Image: The captured screenshot as a PIL Image object.
    """
    try:
        # Take a full screen screenshot
        screenshot = pyautogui.screenshot()
        return screenshot
    except Exception as e:
        print(f"Error taking screenshot: {str(e)}")
        return None


def generate_default_screenshot_name() -> str:
    """
    Generate a default name for saving a screenshot.

    Returns:
    str: The generated default name.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"screenshot_{timestamp}.png"


def generate_default_screenshot_path() -> str:
    """
    Generate a default path for saving a screenshot.

    Returns:
    str: The generated default path.
    """
    default_name = generate_default_screenshot_name()
    return os.path.join(os.getcwd(), default_name)


def save_screenshot(screenshot: Image.Image, save_path: str = None) -> str:
    """
    Save the given screenshot to the specified path or generate a default path.

    Args:
    screenshot (Image.Image): The screenshot to save.
    save_path (str, optional): The file path where the screenshot should be saved.
                               If not provided, a default path will be generated.

    Returns:
    str: The path where the screenshot was saved, or None if saving failed.
    """
    try:
        if not save_path:
            save_path = generate_default_screenshot_path()
        else:
            # Check if the save_path is a directory or an image file
            _, ext = os.path.splitext(save_path)
            if ext.lower() not in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
                # It's a directory, so we need to generate a filename
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                default_name = generate_default_screenshot_name()
                save_path = os.path.join(save_path, default_name)
            else:
                # It's an image file, so we need to ensure the directory exists
                directory = os.path.dirname(save_path)
                if not os.path.exists(directory):
                    os.makedirs(directory)
        
        # Save the screenshot
        screenshot.save(save_path)
        
        return save_path
    except Exception as e:
        print(f"Error saving screenshot: {str(e)}")
        return None
