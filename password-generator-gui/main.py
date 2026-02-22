import tkinter as tk
from tkinter import messagebox
import random
import string

# ---------------- Password Generation Function ---------------- #
def generate_password():
    length = length_slider.get()
    include_numbers = numbers_var.get()
    include_symbols = symbols_var.get()

    characters = string.ascii_letters

    if include_numbers:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation

    if length < 4:
        messagebox.showerror("Error", "Password length must be at least 4.")
        return

    password = ''.join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# ---------------- Copy to Clipboard ---------------- #
def copy_to_clipboard():
    password = password_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "Generate password first!")

# ---------------- Main Window ---------------- #
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("450x500")
root.configure(bg="#F4F6F7")
root.resizable(False, False)

# ---------------- Title ---------------- #
title_label = tk.Label(
    root,
    text="Password Generator",
    font=("Helvetica", 20, "bold"),
    bg="#F4F6F7",
    fg="#2C3E50"
)
title_label.pack(pady=20)

# ---------------- Password Field ---------------- #
password_entry = tk.Entry(
    root,
    font=("Helvetica", 14),
    width=25,
    bd=2,
    relief="groove",
    justify="center"
)
password_entry.pack(pady=15)

# ---------------- Length Slider ---------------- #
length_label = tk.Label(
    root,
    text="Select Password Length:",
    font=("Helvetica", 12),
    bg="#F4F6F7"
)
length_label.pack()

length_slider = tk.Scale(
    root,
    from_=4,
    to=32,
    orient="horizontal",
    length=250,
    bg="#F4F6F7"
)
length_slider.set(12)
length_slider.pack(pady=10)

# ---------------- Options ---------------- #
numbers_var = tk.BooleanVar()
symbols_var = tk.BooleanVar()

numbers_check = tk.Checkbutton(
    root,
    text="Include Numbers",
    variable=numbers_var,
    bg="#F4F6F7",
    font=("Helvetica", 11)
)
numbers_check.pack()

symbols_check = tk.Checkbutton(
    root,
    text="Include Symbols",
    variable=symbols_var,
    bg="#F4F6F7",
    font=("Helvetica", 11)
)
symbols_check.pack()

# ---------------- Buttons ---------------- #
generate_button = tk.Button(
    root,
    text="Generate Password",
    font=("Helvetica", 12, "bold"),
    bg="#3498DB",
    fg="white",
    width=18,
    command=generate_password
)
generate_button.pack(pady=20)

copy_button = tk.Button(
    root,
    text="Copy to Clipboard",
    font=("Helvetica", 12, "bold"),
    bg="#2ECC71",
    fg="white",
    width=18,
    command=copy_to_clipboard
)
copy_button.pack()

# ---------------- Run App ---------------- #
root.mainloop()
