import pyautogui as pg # type: ignore
import time

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