import random
import string
import csv
from tkinter import *
from tkinter import messagebox

class PasswordManager:
    def __init__(self):
        self.passwords = {}

    def add_password(self, website, username, password):
        self.passwords[website] = {'Username': username, 'Password': password}

    def get_password(self, website):
        if website in self.passwords:
            return self.passwords[website]
        else:
            return None

    def delete_password(self, website):
        if website in self.passwords:
            del self.passwords[website]
            
    def generate_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def save_passwords(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Website', 'Username']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for website, password in self.passwords.items():
                writer.writerow({'Website': website, 'Username': password['Username']})

    def load_passwords(self, filename):
        self.passwords = {}
        try:
            with open(filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    website = row['Website']
                    username = row['Username']
                    self.passwords[website] = {'Username': username, 'Password': ''}
        except FileNotFoundError:
            # Если файл не существует, просто проигнорируйте его
            pass

def add_password_gui():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if website and username and password:
        password_manager.add_password(website, username, password)
        messagebox.showinfo("Success", "Password added successfully!")
    else:
        messagebox.showerror("Error", "Please enter all fields.")

    website_entry.delete(0, END)
    username_entry.delete(0, END)
    password_entry.delete(0, END)

def generate_password_gui():
    length_str = length_entry.get()
    if length_str:
        length = int(length_str)
        password = password_manager.generate_password(length)
        password_entry.delete(0, END)
        password_entry.insert(0, password)
    else:
        messagebox.showerror("Error", "Please enter a password length.")

def get_password_gui():
    website = website_entry.get()

    password = password_manager.get_password(website)
    if password:
        messagebox.showinfo("Password", f"Username: {password['Username']}\nPassword: {password['Password']}")
    else:
        messagebox.showerror("Error", "Password not found.")

    website_entry.delete(0, END)

def delete_password_gui():
    website = website_entry.get()

    password_manager.delete_password(website)
    messagebox.showinfo("Success", "Password deleted successfully!")

    website_entry.delete(0, END)

def save_passwords_gui():
    filename = filename_entry.get()
    if filename:
        password_manager.save_passwords(filename)
        messagebox.showinfo("Success", "Passwords saved successfully!")
    else:
        messagebox.showerror("Error", "Please enter a filename.")

def load_passwords_gui():
    filename = filename_entry.get()
    if filename:
        password_manager.load_passwords(filename)
        messagebox.showinfo("Success", "Passwords loaded successfully!")
    else:
        messagebox.showerror("Error", "Please enter a filename.")

# Создание окна
window = Tk()
window.title("Password Manager")
window.geometry("300x400")

# Создание меток и полей ввода
website_label = Label(window, text="Website:")
website_label.pack()
website_entry = Entry(window)
website_entry.pack()

username_label = Label(window, text="Username:")
username_label.pack()
username_entry = Entry(window)
username_entry.pack()

password_label = Label(window, text="Password:")
password_label.pack()
password_entry = Entry(window)
password_entry.pack()

length_label = Label(window, text="Password Length:")
length_label.pack()
length_entry = Entry(window)
length_entry.pack()

# Создание кнопок
add_button = Button(window, text="Add Password", command=add_password_gui)
add_button.pack()

generate_button = Button(window, text="Generate Password", command=generate_password_gui)
generate_button.pack()

get_button = Button(window, text="Get Password", command=get_password_gui)
get_button.pack()

delete_button = Button(window, text="Delete Password", command=delete_password_gui)
delete_button.pack()

save_label = Label(window, text="Save/Load Passwords:")
save_label.pack()
filename_entry = Entry(window)
filename_entry.pack()

save_button = Button(window, text="Save Passwords", command=save_passwords_gui)
save_button.pack()

load_button = Button(window, text="Load Passwords", command=load_passwords_gui)
load_button.pack()

# Создание экземпляра менеджера паролей
password_manager = PasswordManager()

# Запуск цикла обработки событий
window.mainloop()