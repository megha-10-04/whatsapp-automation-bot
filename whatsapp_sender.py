import pywhatkit
import pyautogui
import pyperclip
import time

phone = input("Enter phone number with country code: ")
message = input("Enter message: ")
count = int(input("How many times to send: "))

pyperclip.copy(message)

print("Opening WhatsApp chat...")
pywhatkit.sendwhatmsg_instantly(phone, message, wait_time=15, tab_close=False)

time.sleep(10)

print("Sending messages...")

for i in range(count-1):
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    time.sleep(0.7)

print("Done sending messages!")