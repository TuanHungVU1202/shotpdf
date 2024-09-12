import pyautogui # type: ignore
import os
import tkinter as tk
from PIL import Image
from datetime import datetime
from PIL import ImageGrab
from typing import Tuple, Optional


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


def take_screenshot_roi(roi: Tuple[int, int, int, int]) -> Optional[Image.Image]:
    """
    Take a screenshot of the specified Region of Interest.

    Args:
    roi (Tuple[int, int, int, int]): The coordinates of the ROI (left, top, right, bottom).

    Returns:
    Optional[Image.Image]: The screenshot as a PIL Image object, or None if the screenshot failed.
    """
    try:
        screenshot = ImageGrab.grab(bbox=roi)
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


# Define drawing as a global variable
global drawing
drawing = False

def draw_roi() -> Optional[Tuple[int, int, int, int]]:
    """
    Allow the user to draw a Region of Interest (ROI) on a captured screenshot of the current screen.

    Returns:
    Optional[Tuple[int, int, int, int]]: The coordinates of the ROI (left, top, right, bottom),
                                         or None if the selection was cancelled.
    """
    global drawing
    # Capture the current screen and save it to a temporary file
    screenshot = ImageGrab.grab()
    temp_screenshot = os.path.join(os.getcwd(), "temp_screenshot.png")
    screenshot.save(temp_screenshot)

    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)

    # Open the temporary image file
    photo = tk.PhotoImage(file=temp_screenshot)

    roi_coords = [0, 0, 0, 0]
    drawing = False

    canvas = tk.Canvas(root, highlightthickness=0, cursor="cross")
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)

    canvas.bind("<ButtonPress-1>", lambda event: on_press(event, roi_coords))
    canvas.bind("<ButtonRelease-1>", lambda event: on_release(event, roi_coords, root))
    canvas.bind("<B1-Motion>", lambda event: on_motion(event, canvas, roi_coords))
    root.bind("<Escape>", lambda e: root.destroy())

    root.mainloop()
    
    # Delete the temporary screenshot file
    os.remove(temp_screenshot)

    if roi_coords[2] == 0 and roi_coords[3] == 0:
        return None
    return tuple(roi_coords)


def on_press(event, roi_coords):
    global drawing
    roi_coords[0], roi_coords[1] = event.x, event.y
    drawing = True

def on_release(event, roi_coords, root):
    global drawing
    roi_coords[2], roi_coords[3] = event.x, event.y
    drawing = False
    root.destroy()

def on_motion(event, canvas, roi_coords):
    global drawing
    if drawing:
        canvas.delete("roi")
        canvas.create_rectangle(roi_coords[0], roi_coords[1], event.x, event.y, 
                                outline="red", width=2, tags="roi", dash=(4, 4))
