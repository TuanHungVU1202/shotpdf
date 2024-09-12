import multiprocessing
import sys
import time
import os
from typing import Optional, Tuple
from service.screenshooter import draw_roi, take_screenshot, save_screenshot, take_screenshot_roi
from service.pdf_handler import save_images_to_pdf
from service.input_simulator import *


def parse_arguments():
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
    pdf_path = os.path.join(save_directory, "output.pdf")
    save_images_to_pdf(save_directory, pdf_path)
    print(f"PDF saved to {pdf_path}")


def main():
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