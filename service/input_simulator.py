import pyautogui as pg # type: ignore
import time
import json
import logging


def input_simulator_health():
    """
    Perform a health check for the Input Simulator.

    This function prints a message indicating that the Input Simulator health check is being performed.
    """
    print("Input Simulator Health Check")


def simulate_with_config(config):
    """
    Simulate key presses based on the provided configuration.

    Args:
    config (dict): A dictionary containing the simulation configuration.
                   Expected keys: 'skey', 'delay_before', 'delay_after', 'repeat'

    The function validates the input, then simulates key presses according to the configuration.
    It logs an error if the input is invalid or if the required 'skey' is missing.
    """
    if not isinstance(config, dict):
        logging.error("Input is not a valid JSON-like object")
        return

    skey = config.get('skey')
    delay_before = config.get('delay_before', 0)
    delay_after = config.get('delay_after', 0)
    repeat = config.get('repeat', 1)

    if not skey:
        logging.error("No 'skey' found in the input object")
        return

    for _ in range(repeat):
        time.sleep(delay_before)
        pg.press(skey)
        time.sleep(delay_after)


def simulate_key(key: str):
    """
    Simulate a single key press.

    Args:
    key (str): The key to be pressed.

    The function checks if the input is a valid string and logs an error if it's not.
    If valid, it simulates pressing the specified key.
    """
    if not isinstance(key, str):
        logging.error("Input is not a valid string")
        return

    pg.press(key)


def simulate_page_up_down():
    """
    Simulate pressing Page Down and Page Up keys with delays.

    This function waits for 5 seconds, then simulates pressing the Page Down key,
    waits for 1 second, simulates pressing the Page Up key, and waits for another second.
    """
    time.sleep(5) 
    # Simulate pressing Page Down
    pg.press('pagedown')
    time.sleep(1)  # Wait for 1 second

    # Simulate pressing Page Up
    pg.press('pagedup')
    time.sleep(1)  # Wait for 1 second


def parse_json_file(path: str):
    """
    Parse a JSON file and extract specific keys.

    Args:
    path (str): The file path of the JSON file to be parsed.

    Returns:
    dict: A dictionary containing the parsed data with specific keys.

    This function attempts to read and parse a JSON file, extracting only specific
    valid keys. It handles various exceptions and logs errors accordingly.
    """
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

    This function creates a copy of the input object, replaces or adds the specified
    key-value pair, and returns the new object. It logs warnings or errors as needed.
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
