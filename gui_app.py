import tkinter as tk
from tkinter import messagebox
import csv
import pywhatkit
import pyautogui
import pyperclip
import time


# Create main window
root = tk.Tk()
root.title("WhatsApp Manager")
root.geometry("400x500")

# Title
title = tk.Label(root, text="WhatsApp Manager", font=("Arial", 18, "bold"))
title.pack(pady=20)

def add_contact_gui():
    def save_contact():
        name = entry_name.get()
        phone = entry_phone.get()

        if name == "" or phone == "":
            messagebox.showerror("Error", "All fields are required")
            return

        with open("contacts.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, phone])

        messagebox.showinfo("Success", "Contact saved!")
        add_window.destroy()

    # New popup window
    add_window = tk.Toplevel(root)
    add_window.title("Add Contact")
    add_window.geometry("300x200")

    tk.Label(add_window, text="Name").pack(pady=5)
    entry_name = tk.Entry(add_window, width=30)
    entry_name.pack(pady=5)

    tk.Label(add_window, text="Phone").pack(pady=5)
    entry_phone = tk.Entry(add_window, width=30)
    entry_phone.pack(pady=5)

    tk.Button(add_window, text="Save", command=save_contact).pack(pady=10)

def show_contacts_gui():
    try:
        with open("contacts.csv", "r") as file:
            reader = csv.reader(file)
            contacts = list(reader)

        if not contacts:
            messagebox.showinfo("Info", "No contacts found")
            return

        # Create new window
        show_window = tk.Toplevel(root)
        show_window.title("Contacts")
        show_window.geometry("300x300")

        tk.Label(show_window, text="Contact List", font=("Arial", 14)).pack(pady=10)

        # Listbox to display contacts
        listbox = tk.Listbox(show_window, width=40)
        listbox.pack(pady=10)

        for contact in contacts:
            listbox.insert(tk.END, f"{contact[0]} - {contact[1]}")

    except FileNotFoundError:
        messagebox.showerror("Error", "contacts.csv not found")

def delete_contact_gui():
    try:
        with open("contacts.csv", "r") as file:
            reader = csv.reader(file)
            contacts = list(reader)

        if not contacts:
            messagebox.showinfo("Info", "No contacts to delete")
            return

        # New window
        delete_window = tk.Toplevel(root)
        delete_window.title("Delete Contact")
        delete_window.geometry("300x300")

        tk.Label(delete_window, text="Select Contact to Delete", font=("Arial", 12)).pack(pady=10)

        listbox = tk.Listbox(delete_window, width=40)
        listbox.pack(pady=10)

        for contact in contacts:
            listbox.insert(tk.END, f"{contact[0]} - {contact[1]}")

        def delete_selected():
            selected_index = listbox.curselection()

            if not selected_index:
                messagebox.showerror("Error", "Select a contact first")
                return

            index = selected_index[0]
            deleted = contacts.pop(index)

            with open("contacts.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(contacts)

            messagebox.showinfo("Success", f"Deleted: {deleted[0]}")
            delete_window.destroy()

        tk.Button(delete_window, text="Delete", command=delete_selected).pack(pady=10)

    except FileNotFoundError:
        messagebox.showerror("Error", "contacts.csv not found")

def send_message_gui():
    try:
        with open("contacts.csv", "r") as file:
            reader = csv.reader(file)
            contacts = list(reader)

        if not contacts:
            messagebox.showinfo("Info", "No contacts found")
            return

        # New window
        send_window = tk.Toplevel(root)
        send_window.title("Send Message")
        send_window.geometry("350x400")

        tk.Label(send_window, text="Select Contact(s)", font=("Arial", 12)).pack(pady=5)

        listbox = tk.Listbox(send_window, selectmode=tk.MULTIPLE, width=40)
        listbox.pack(pady=10)

        for contact in contacts:
            listbox.insert(tk.END, f"{contact[0]} - {contact[1]}")

        tk.Label(send_window, text="Message").pack()
        entry_message = tk.Entry(send_window, width=40)
        entry_message.pack(pady=5)

        tk.Label(send_window, text="Count").pack()
        entry_count = tk.Entry(send_window, width=10)
        entry_count.pack(pady=5)

        def send_now():
            selected = listbox.curselection()

            if not selected:
                messagebox.showerror("Error", "Select at least one contact")
                return

            message = entry_message.get()
            count = int(entry_count.get())

            pyperclip.copy(message)

            for i in selected:
                name = contacts[i][0]
                phone = contacts[i][1]

                messagebox.showinfo("Sending", f"Sending to {name}...")

                pywhatkit.sendwhatmsg_instantly(phone, message, wait_time=15, tab_close=False)
                time.sleep(10)

                for _ in range(count - 1):
                    pyautogui.hotkey("ctrl", "v")
                    pyautogui.press("enter")
                    time.sleep(0.7)

                time.sleep(2)
                pyautogui.hotkey("alt", "tab")
                time.sleep(1)
                pyautogui.hotkey("alt", "shift", "tab")
                time.sleep(1)

            messagebox.showinfo("Done", "Messages sent successfully!")

        tk.Button(send_window, text="Send", command=send_now).pack(pady=15)

    except FileNotFoundError:
        messagebox.showerror("Error", "contacts.csv not found")

def schedule_message_gui():
    try:
        with open("contacts.csv", "r") as file:
            reader = csv.reader(file)
            contacts = list(reader)

        if not contacts:
            messagebox.showinfo("Info", "No contacts found")
            return

        # New window
        schedule_window = tk.Toplevel(root)
        schedule_window.title("Schedule Message")
        schedule_window.geometry("350x400")

        tk.Label(schedule_window, text="Select Contact(s)", font=("Arial", 12)).pack(pady=5)

        listbox = tk.Listbox(schedule_window, selectmode=tk.MULTIPLE, width=40)
        listbox.pack(pady=10)

        for contact in contacts:
            listbox.insert(tk.END, f"{contact[0]} - {contact[1]}")

        tk.Label(schedule_window, text="Message").pack()
        entry_message = tk.Entry(schedule_window, width=40)
        entry_message.pack(pady=5)

        tk.Label(schedule_window, text="Hour (0-23)").pack()
        entry_hour = tk.Entry(schedule_window, width=10)
        entry_hour.pack(pady=5)

        tk.Label(schedule_window, text="Minute (0-59)").pack()
        entry_minute = tk.Entry(schedule_window, width=10)
        entry_minute.pack(pady=5)

        def schedule_now():
            selected = listbox.curselection()

            if not selected:
                messagebox.showerror("Error", "Select at least one contact")
                return

            message = entry_message.get()
            hour = int(entry_hour.get())
            minute = int(entry_minute.get())

            for i in selected:
                name = contacts[i][0]
                phone = contacts[i][1]

                messagebox.showinfo("Scheduled", f"Scheduled for {name} at {hour:02d}:{minute:02d}")

                pywhatkit.sendwhatmsg(phone, message, hour, minute, wait_time=15, tab_close=False)

            messagebox.showinfo("Done", "All messages scheduled!")

        tk.Button(schedule_window, text="Schedule", command=schedule_now).pack(pady=15)

    except FileNotFoundError:
        messagebox.showerror("Error", "contacts.csv not found")

# Buttons (for now just placeholders)
btn_add = tk.Button(root, text="Add Contact", width=25, height=2, command=add_contact_gui)
btn_add.pack(pady=10)

btn_show = tk.Button(root, text="Show Contacts", width=25, height=2, command=show_contacts_gui)
btn_show.pack(pady=10)

btn_send = tk.Button(root, text="Send Message", width=25, height=2, command=send_message_gui)
btn_send.pack(pady=10)

btn_schedule = tk.Button(root, text="Schedule Message", width=25, height=2)
btn_schedule.pack(pady=10)

btn_delete = tk.Button(root, text="Delete Contact", width=25, height=2, command=delete_contact_gui)
btn_delete.pack(pady=10)

# Run app
root.mainloop()