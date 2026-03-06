import tkinter as tk
from tkinter import messagebox
import random
import string

# -------- Hover Effects -------- #
def hover_generate(e):
    generate_button["bg"] = "#1ABC9C"

def leave_generate(e):
    generate_button["bg"] = "#16A085"

def hover_copy(e):
    copy_button["bg"] = "#2980B9"

def leave_copy(e):
    copy_button["bg"] = "#3498DB"


# -------- Password Generator -------- #
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
        messagebox.showerror("Error", "Password length must be at least 4")
        return

    password = ''.join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)


# -------- Copy Password -------- #
def copy_to_clipboard():
    password = password_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "Generate password first!")


# -------- Main Window -------- #
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("450x520")
root.configure(bg="#2C3E50")
root.resizable(False, False)

# -------- Title -------- #
title = tk.Label(
    root,
    text="Password Generator",
    font=("Segoe UI", 22, "bold"),
    bg="#2C3E50",
    fg="white"
)
title.pack(pady=25)

# -------- Card Frame -------- #
frame = tk.Frame(root, bg="#34495E", padx=25, pady=25)
frame.pack(pady=10)

# -------- Password Field -------- #
password_entry = tk.Entry(
    frame,
    font=("Segoe UI", 14),
    width=24,
    justify="center",
    bd=2
)
password_entry.pack(pady=10)

# -------- Length -------- #
length_label = tk.Label(
    frame,
    text="Select Password Length",
    font=("Segoe UI", 11),
    bg="#34495E",
    fg="white"
)
length_label.pack()

length_slider = tk.Scale(
    frame,
    from_=4,
    to=32,
    orient="horizontal",
    length=250,
    bg="#34495E",
    fg="white",
    highlightthickness=0
)
length_slider.set(12)
length_slider.pack(pady=10)

# -------- Options -------- #
numbers_var = tk.BooleanVar()
symbols_var = tk.BooleanVar()

numbers_check = tk.Checkbutton(
    frame,
    text="Include Numbers",
    variable=numbers_var,
    font=("Segoe UI", 11),
    bg="#34495E",
    fg="white",
    selectcolor="#34495E"
)
numbers_check.pack(anchor="w")

symbols_check = tk.Checkbutton(
    frame,
    text="Include Symbols",
    variable=symbols_var,
    font=("Segoe UI", 11),
    bg="#34495E",
    fg="white",
    selectcolor="#34495E"
)
symbols_check.pack(anchor="w")

# -------- Buttons -------- #
generate_button = tk.Button(
    root,
    text="Generate Password",
    font=("Segoe UI", 12, "bold"),
    bg="#16A085",
    fg="white",
    width=20,
    command=generate_password
)
generate_button.pack(pady=20)

generate_button.bind("<Enter>", hover_generate)
generate_button.bind("<Leave>", leave_generate)

copy_button = tk.Button(
    root,
    text="Copy to Clipboard",
    font=("Segoe UI", 12, "bold"),
    bg="#3498DB",
    fg="white",
    width=20,
    command=copy_to_clipboard
)
copy_button.pack()

copy_button.bind("<Enter>", hover_copy)
copy_button.bind("<Leave>", leave_copy)

# -------- Run App -------- #
root.mainloop()
