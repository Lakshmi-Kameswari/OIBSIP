import tkinter as tk
from tkinter import messagebox

# ---------- Hover Effects ---------- #
def on_enter(e):
    e.widget['background'] = '#1ABC9C'

def on_leave(e):
    e.widget['background'] = '#16A085'

def on_enter_reset(e):
    e.widget['background'] = '#C0392B'

def on_leave_reset(e):
    e.widget['background'] = '#E74C3C'


# ---------- BMI Calculation ---------- #
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height_cm = float(height_entry.get())

        if weight <= 0 or height_cm <= 0:
            messagebox.showerror("Invalid Input", "Enter positive values")
            return

        height_m = height_cm / 100
        bmi = round(weight / (height_m ** 2), 2)

        if bmi < 18.5:
            category = "Underweight"
            color = "#F39C12"
        elif bmi < 24.9:
            category = "Normal Weight"
            color = "#27AE60"
        elif bmi < 29.9:
            category = "Overweight"
            color = "#E67E22"
        else:
            category = "Obese"
            color = "#E74C3C"

        result_label.config(
            text=f"BMI: {bmi}\nCategory: {category}",
            fg=color
        )

    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers")


# ---------- Reset ---------- #
def reset_fields():
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    result_label.config(text="")


# ---------- Main Window ---------- #
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("420x480")
root.configure(bg="#2C3E50")
root.resizable(False, False)

# ---------- Title ---------- #
title = tk.Label(
    root,
    text="BMI Calculator",
    font=("Segoe UI", 22, "bold"),
    bg="#2C3E50",
    fg="white"
)
title.pack(pady=25)

# ---------- Frame ---------- #
frame = tk.Frame(root, bg="#34495E", padx=20, pady=20)
frame.pack(pady=10)

# ---------- Weight ---------- #
weight_label = tk.Label(
    frame,
    text="Weight (kg)",
    font=("Segoe UI", 12),
    bg="#34495E",
    fg="white"
)
weight_label.grid(row=0, column=0, pady=10)

weight_entry = tk.Entry(
    frame,
    font=("Segoe UI", 12),
    width=20,
    bd=2
)
weight_entry.grid(row=0, column=1)

# ---------- Height ---------- #
height_label = tk.Label(
    frame,
    text="Height (cm)",
    font=("Segoe UI", 12),
    bg="#34495E",
    fg="white"
)
height_label.grid(row=1, column=0, pady=10)

height_entry = tk.Entry(
    frame,
    font=("Segoe UI", 12),
    width=20,
    bd=2
)
height_entry.grid(row=1, column=1)

# ---------- Buttons ---------- #
button_frame = tk.Frame(root, bg="#2C3E50")
button_frame.pack(pady=20)

calculate_btn = tk.Button(
    button_frame,
    text="Calculate",
    font=("Segoe UI", 12, "bold"),
    bg="#16A085",
    fg="white",
    width=12,
    command=calculate_bmi
)
calculate_btn.grid(row=0, column=0, padx=10)

calculate_btn.bind("<Enter>", on_enter)
calculate_btn.bind("<Leave>", on_leave)

reset_btn = tk.Button(
    button_frame,
    text="Reset",
    font=("Segoe UI", 12, "bold"),
    bg="#E74C3C",
    fg="white",
    width=12,
    command=reset_fields
)
reset_btn.grid(row=0, column=1, padx=10)

reset_btn.bind("<Enter>", on_enter_reset)
reset_btn.bind("<Leave>", on_leave_reset)

# ---------- Result ---------- #
result_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 16, "bold"),
    bg="#2C3E50",
    fg="white"
)
result_label.pack(pady=25)

root.mainloop()
