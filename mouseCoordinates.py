import pyautogui
import keyboard
import time


time.sleep(1)

while True:
    if keyboard.is_pressed('z'):
        position = pyautogui.position()
        print(position)
        