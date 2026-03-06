import tkinter as tk
from tkinter import messagebox
import random
import string

# -------- Hover Effects -------- #
def hover_generate(e):
    generate_button["bg"] = "#ff4da6"

def leave_generate(e):
    generate_button["bg"] = "#ff66b2"

def hover_copy(e):
    copy_button["bg"] = "#3399ff"

def leave_copy(e):
    copy_button["bg"] = "#4da6ff"


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
root.configure(bg="#1E3A5F")   # Dark Blue Background
root.resizable(False, False)

# -------- Title -------- #
title = tk.Label(
    root,
    text="🔐 Password Generator",
    font=("Segoe UI", 22, "bold"),
    bg="#1E3A5F",
    fg="#FFD700"  # Gold Yellow
)
title.pack(pady=25)

# -------- Card Frame -------- #
frame = tk.Frame(root, bg="#5DADE2", padx=25, pady=25)  # Light Blue
frame.pack(pady=10)

# -------- Password Field -------- #
password_entry = tk.Entry(
    frame,
    font=("Segoe UI", 14),
    width=24,
    justify="center",
    bd=3,
    bg="#FDEBD0"   # Light Yellow
)
password_entry.pack(pady=10)

# -------- Length -------- #
length_label = tk.Label(
    frame,
    text="Select Password Length",
    font=("Segoe UI", 11, "bold"),
    bg="#5DADE2",
    fg="black"
)
length_label.pack()

length_slider = tk.Scale(
    frame,
    from_=4,
    to=32,
    orient="horizontal",
    length=250,
    bg="#5DADE2",
    fg="black",
    highlightthickness=0,
    troughcolor="#82E0AA"  # Light Green
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
    bg="#5DADE2",
    fg="black",
    selectcolor="#82E0AA"
)
numbers_check.pack(anchor="w")

symbols_check = tk.Checkbutton(
    frame,
    text="Include Symbols",
    variable=symbols_var,
    font=("Segoe UI", 11),
    bg="#5DADE2",
    fg="black",
    selectcolor="#82E0AA"
)
symbols_check.pack(anchor="w")

# -------- Generate Button -------- #
generate_button = tk.Button(
    root,
    text="Generate Password",
    font=("Segoe UI", 12, "bold"),
    bg="#FF5F1F",   # Pink
    fg="white",
    width=20,
    command=generate_password
)
generate_button.pack(pady=20)

generate_button.bind("<Enter>", hover_generate)
generate_button.bind("<Leave>", leave_generate)

# -------- Copy Button -------- #
copy_button = tk.Button(
    root,
    text="Copy to Clipboard",
    font=("Segoe UI", 12, "bold"),
    bg="#4da6ff",   # Blue
    fg="white",
    width=20,
    command=copy_to_clipboard
)
copy_button.pack()

copy_button.bind("<Enter>", hover_copy)
copy_button.bind("<Leave>", leave_copy)

# -------- Footer -------- #
footer = tk.Label(
    root,
    text="Secure • Fast • Easy",
    font=("Segoe UI", 10),
    bg="#1E3A5F",
    fg="#82E0AA"
)
footer.pack(pady=15)

# -------- Run App -------- #
root.mainloop()
