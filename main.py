import multiprocessing
import sys
import time
import os
from typing import Optional, Tuple
from service.screenshooter import draw_roi, take_screenshot, save_screenshot, take_screenshot_roi
from service.pdf_handler import save_images_to_pdf
from service.input_simulator import *


def parse_arguments():
    """
    Parse command-line arguments for the script.

    This function processes the command-line arguments to determine:
    - The number of times to repeat the screenshot and key press process.
    - The directory where screenshots and the final PDF should be saved.
    - Whether to capture fullscreen screenshots or a region of interest.

    If the repeat count is not provided, it uses a default value from a JSON configuration file.
    If the specified save directory doesn't exist, it attempts to create it.

    Returns:
        tuple: A tuple containing (repeat_count, save_directory, fullscreen_mode).

    Raises:
        SystemExit: If required arguments are missing or if there's an error creating the save directory.
    """
    if len(sys.argv) < 3:
        print("Usage: python main.py -c <repeat_count> -d <save_directory> [-r]")
        sys.exit(1)

    repeat = None
    save_directory = None
    fullscreen = True

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '-c':
            if i + 1 < len(sys.argv):
                repeat = int(sys.argv[i + 1])
                i += 2
            else:
                print("Error: -c option requires a value")
                sys.exit(1)
        elif sys.argv[i] == '-d':
            if i + 1 < len(sys.argv):
                save_directory = sys.argv[i + 1]
                i += 2
            else:
                print("Error: -d option requires a value")
                sys.exit(1)
        elif sys.argv[i] == '-r':
            fullscreen = False
            i += 1
        else:
            i += 1

    if save_directory is None or save_directory.strip() == '':
        print("Save directory must be provided and cannot be blank.")
        sys.exit(1)
    
    if repeat is None:
        json_data = parse_json_file('resources/single_key.json')
        print(f"Repeat count not provided. Using default value from JSON: {json_data.get('repeat', 1)}")
        repeat = json_data.get('repeat', 1)

    if not os.path.exists(save_directory):
        try:
            os.makedirs(save_directory)
            print(f"Created directory: {save_directory}")
        except OSError as e:
            print(f"Error creating directory {save_directory}: {e}")
            sys.exit(1)

    return repeat, save_directory, fullscreen


def simulate_keys_and_take_screenshots(
        repeat: int, 
        save_directory: str, 
        roi: Optional[Tuple[int, int, int, int]] = None
    ):
    """
    Simulate key presses and capture screenshots for a specified number of iterations.

    This function performs the following steps for each iteration:
    1. Waits for a specified delay before taking a screenshot.
    2. Captures a screenshot (either fullscreen or of a specified region).
    3. Saves the screenshot to the specified directory.
    4. Simulates a key press based on the configuration in 'resources/single_key.json'.
    5. Waits for a specified delay after the key press.

    Args:
        repeat (int): Number of times to repeat the process.
        save_directory (str): Directory to save the captured screenshots.
        roi (Optional[Tuple[int, int, int, int]]): Region of interest for screenshots. If None, captures fullscreen.

    Note:
        The function reads key press and delay configurations from 'resources/single_key.json'.
    """
    
    json_data = parse_json_file('resources/single_key.json')
    json_data['delay_before'] = 1
    json_data['delay_after'] = 1

    print("Waiting 5 seconds before starting...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    for i in range(repeat):
        time.sleep(json_data['delay_before'])
        
        print(f"Take screenshot {i+1}/{repeat}")
        screenshot = None
        
        if roi is None:
            screenshot = take_screenshot()
        else:
            screenshot = take_screenshot_roi(roi)

        if screenshot:
            save_path = os.path.join(save_directory, f"screenshot_{i+1}.png")
            save_screenshot(screenshot, save_path)
        else:
            print(f"Failed to take screenshot on iteration {i+1}")

        simulate_key(json_data['skey'])
        time.sleep(json_data['delay_after'])


def save_images_to_pdf_file(save_directory: str):
    """
    Compile all captured screenshots in the save directory into a single PDF file.

    This function:
    1. Determines the path for the output PDF file.
    2. Calls the 'save_images_to_pdf' function to create the PDF from the screenshots.
    3. Prints a confirmation message with the path of the saved PDF.

    Args:
        save_directory (str): Directory containing the screenshot images.

    Note:
        The output PDF will be named 'output.pdf' and saved in the same directory as the screenshots.
    """
    pdf_path = os.path.join(save_directory, "output.pdf")
    save_images_to_pdf(save_directory, pdf_path)
    print(f"PDF saved to {pdf_path}")


def main():
    """
    Main function to orchestrate the screenshot capture and key simulation process.

    This function:
    1. Parses command-line arguments to get process parameters.
    2. If not in fullscreen mode, uses multiprocessing to allow the user to select a region of interest.
    3. Waits for 10 seconds before starting the main process.
    4. Calls the function to simulate key presses and take screenshots.
    5. Compiles all captured screenshots into a single PDF file.

    Note:
        Multiprocessing is used for the ROI selection to handle potential GUI operations safely.
    """
    repeat, save_directory, fullscreen = parse_arguments()

    roi = None
    if not fullscreen:
        with multiprocessing.Pool(processes=1) as pool:
            roi = pool.apply(draw_roi)
    
    print("Waiting 10 seconds before starting...")
    time.sleep(10)
    simulate_keys_and_take_screenshots(repeat, save_directory, roi)
    save_images_to_pdf_file(save_directory)


if __name__ == "__main__":
    main()