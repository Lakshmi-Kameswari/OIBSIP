import tkinter as tk
from tkinter import messagebox

# -------------------- BMI Calculation Function -------------------- #
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height_cm = float(height_entry.get())

        if weight <= 0 or height_cm <= 0:
            messagebox.showerror("Invalid Input", "Height and Weight must be positive values.")
            return

        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)
        bmi = round(bmi, 2)

        category = ""
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal Weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

        result_label.config(
            text=f"Your BMI: {bmi}\nCategory: {category}",
            fg="#2E8B57"
        )

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values.")


# -------------------- Reset Function -------------------- #
def reset_fields():
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    result_label.config(text="")


# -------------------- Main Window -------------------- #
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("400x450")
root.configure(bg="#F4F6F7")
root.resizable(False, False)

# -------------------- Title -------------------- #
title_label = tk.Label(
    root,
    text="BMI Calculator",
    font=("Helvetica", 20, "bold"),
    bg="#F4F6F7",
    fg="#2C3E50"
)
title_label.pack(pady=20)

# -------------------- Weight Input -------------------- #
weight_label = tk.Label(
    root,
    text="Enter Weight (kg):",
    font=("Helvetica", 12),
    bg="#F4F6F7"
)
weight_label.pack(pady=5)

weight_entry = tk.Entry(
    root,
    font=("Helvetica", 12),
    width=20,
    bd=2,
    relief="groove"
)
weight_entry.pack(pady=5)

# -------------------- Height Input -------------------- #
height_label = tk.Label(
    root,
    text="Enter Height (cm):",
    font=("Helvetica", 12),
    bg="#F4F6F7"
)
height_label.pack(pady=5)

height_entry = tk.Entry(
    root,
    font=("Helvetica", 12),
    width=20,
    bd=2,
    relief="groove"
)
height_entry.pack(pady=5)

# -------------------- Buttons -------------------- #
button_frame = tk.Frame(root, bg="#F4F6F7")
button_frame.pack(pady=20)

calculate_button = tk.Button(
    button_frame,
    text="Calculate",
    font=("Helvetica", 12, "bold"),
    bg="#3498DB",
    fg="white",
    width=10,
    command=calculate_bmi
)
calculate_button.grid(row=0, column=0, padx=10)

reset_button = tk.Button(
    button_frame,
    text="Reset",
    font=("Helvetica", 12, "bold"),
    bg="#E74C3C",
    fg="white",
    width=10,
    command=reset_fields
)
reset_button.grid(row=0, column=1, padx=10)

# -------------------- Result -------------------- #
result_label = tk.Label(
    root,
    text="",
    font=("Helvetica", 14, "bold"),
    bg="#F4F6F7"
)
result_label.pack(pady=20)

# -------------------- Run App -------------------- #
root.mainloop()
