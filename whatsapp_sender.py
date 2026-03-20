import pywhatkit
import pyautogui
import pyperclip
import time
import csv
from datetime import datetime

def add_contact():
    name = input("Enter contact name: ")
    phone = input("Enter phone number with country code: ")

    with open("contacts.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, phone])

    print("✅ Contact saved!")

def show_contacts():
    try:
        with open("contacts.csv", "r") as file:
            reader = csv.reader(file)
            contacts = list(reader)

            if not contacts:
                print("⚠ No contacts found")
                return []

            print("\n📋 Contact List:")
            for i, contact in enumerate(contacts):
                print(f"{i + 1}. {contact[0]} - {contact[1]}")

            return contacts

    except FileNotFoundError:
        print("⚠ contacts.csv not found")
        return []

def delete_contact():
    contacts = show_contacts()

    if not contacts:
        return

    try:
        choice = int(input("Enter contact number to delete: "))

        if choice < 1 or choice > len(contacts):
            print("❌ Invalid choice")
            return

        deleted = contacts.pop(choice - 1)

        with open("contacts.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(contacts)

        print(f"🗑 Deleted contact: {deleted[0]}")

    except:
        print("❌ Invalid choice")


# ✅ MODIFIED FUNCTION (single + multiple combined)
def select_contact():
    contacts = show_contacts()

    if not contacts:
        return []

    choices = input("Select contact number(s) (e.g. 1 or 1,3): ")

    selected = []

    try:
        indexes = choices.split(",")

        for i in indexes:
            index = int(i.strip()) - 1
            selected.append(contacts[index])

        return selected

    except:
        print("❌ Invalid choice")
        return []

def log_message(name):
    current_time = datetime.now().strftime("%I:%M %p")

    log_text = f"Message sent to {name} at {current_time} ✔"

    print(log_text)

    with open("log.txt", "a", encoding="utf-8") as file:
        file.write(log_text + "\n")


def open_whatsapp(phone, message):
    print("Opening WhatsApp chat...")
    pywhatkit.sendwhatmsg_instantly(phone, message, wait_time=15, tab_close=False)


def send_remaining_messages(count):
    print("Sending messages...")

    for i in range(count - 1):
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")
        time.sleep(0.7)

    print("Done sending messages!")

def schedule_message(phone, message, hour, minute):
    print(f"⏰ Message scheduled at {hour:02d}:{minute:02d}")

    pywhatkit.sendwhatmsg(phone, message, hour, minute, wait_time=15, tab_close=False)

def main():
    while True:
        print("\n===== MENU =====")
        print("1. Add Contact")
        print("2. Show Contacts")
        print("3. Send Message")
        print("4. Schedule Message")
        print("5. Delete Contact")   # 👈 ADD
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            add_contact()

        elif choice == "2":
            show_contacts()

        elif choice == "3":
            contacts = select_contact()
            if not contacts:
                continue

            message = input("Enter message: ")
            count = int(input("How many times to send: "))

            pyperclip.copy(message)

            if len(contacts) > 1:
                print("🚀 Sending to multiple contacts...")
            else:
                print("🚀 Sending to selected contact...")

            for contact in contacts:
                name = contact[0]
                phone = contact[1]

                print(f"\n📤 Sending to {name}...")

                open_whatsapp(phone, message)
                time.sleep(10)
                send_remaining_messages(count)

                time.sleep(2)

                pyautogui.hotkey("alt", "tab")
                time.sleep(1)
                pyautogui.hotkey("alt", "shift", "tab")
                time.sleep(1)

                print("Returned to terminal ✅")

                log_message(name)

                time.sleep(2)

        elif choice == "4":
            contacts = select_contact()

            if not contacts:
                continue

            message = input("Enter message: ")

            hour = int(input("Enter hour (0-23): "))
            minute = int(input("Enter minute (0-59): "))

            for contact in contacts:
                name = contact[0]
                phone = contact[1]

                print(f"⏰ Scheduling for {name}...")

                schedule_message(phone, message, hour, minute)

                log_message(name)


        elif choice == "5":
            delete_contact()

        elif choice == "6":   # ✅ updated
            print("Exiting...")
            break

        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main()