import sys
import time
import os
from service.screenshooter import take_screenshot, save_screenshot
from service.pdf_handler import save_images_to_pdf
from service.input_simulator import *
from service.input_simulator import parse_json_file, simulate_key


def main():
    json_data = parse_json_file('resources/single_key.json')
    json_data['delay_before'] = 0.5
    json_data['delay_after'] = 0.5
    
    if len(sys.argv) < 3:
        print("Usage: python main.py -c <repeat_count> -d <save_directory>")

    repeat = None
    save_directory = None

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
        else:
            i += 1

    if save_directory is None:
        print("Save directory must be provided.")
        sys.exit(1)
    
    if repeat is None:
        print(f"Repeat count not provided. Using default value from JSON: {json_data.get('repeat', 1)}")
        repeat = json_data.get('repeat', 1)

    if not save_directory or save_directory.strip() == '':
        print("Save directory not provided or is blank. Terminating.")
        sys.exit(1)
    
    if not os.path.exists(save_directory):
        try:
            os.makedirs(save_directory)
            print(f"Created directory: {save_directory}")
        except OSError as e:
            print(f"Error creating directory {save_directory}: {e}")
            sys.exit(1)

    print("Waiting 5 seconds before starting...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    for i in range(repeat):
        print(f"Take screenshot {i+1}/{repeat}")
        time.sleep(json_data['delay_before'])
        simulate_key(json_data['skey'])
        time.sleep(json_data['delay_after'])
        
        screenshot = take_screenshot()
        if screenshot:
            save_path = os.path.join(save_directory, f"screenshot_{i+1}.png")
            save_screenshot(screenshot, save_path)
        else:
            print(f"Failed to take screenshot on iteration {i+1}")

    pdf_path = os.path.join(save_directory, "output.pdf")
    save_images_to_pdf(save_directory, pdf_path)
    print(f"PDF saved to {pdf_path}")


if __name__ == "__main__":
    main()