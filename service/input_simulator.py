import pyautogui as pg # type: ignore
import time
import json
import logging


def input_simulator_health():
    print("Input Simulator Health Check")

    
def simulate_page_up_down():
    time.sleep(5) 
    # Simulate pressing Page Down
    pg.press('pagedown')
    time.sleep(1)  # Wait for 1 second

    # Simulate pressing Page Up
    pg.press('pagedup')
    time.sleep(1)  # Wait for 1 second


def parse_json_file(path: str):
    try:
        with open(path, 'r') as file:
            data = json.load(file)
        
        valid_keys = ['skey', 'delay_before', 'delay_after', 'wait_event', 'repeat']
        parsed_data = {key: data[key] for key in valid_keys if key in data}

        return parsed_data
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in file: {path}")
        return {}
    except FileNotFoundError:
        logging.error(f"File not found: {path}")
        return {}
    except Exception as e:
        logging.error(f"An error occurred while parsing the JSON file: {str(e)}")
        return {}


def replace_json_value(json_object, new_key, new_value):
    """
    Replace a specific value from a key-value pair in a JSON-like object.

    Args:
    json_object (dict): The JSON-like object returned from parse_json_file function.
    new_key (str): The key whose value needs to be replaced.
    new_value: The new value to be set for the specified key.

    Returns:
    dict: A new object with all key-value pairs, including the replaced one.
    """
    if not isinstance(json_object, dict):
        logging.error("Input is not a valid JSON-like object")
        return {}

    new_object = json_object.copy()
    if new_key in new_object:
        new_object[new_key] = new_value
    else:
        logging.warning(f"Key '{new_key}' not found in the JSON object. Adding it as a new key-value pair.")
        new_object[new_key] = new_value

    return new_object
