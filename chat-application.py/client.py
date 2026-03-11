import socket
import threading
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import re
from config import HOST, PORT, BUFFER_SIZE


class ModernChatApp:

    BG_DARK = "#0D1117"
    BG_MID = "#161B22"
    BG_CARD = "#1C2333"
    ACCENT = "#58A6FF"
    ACCENT2 = "#3FB950"
    TEXT_MAIN = "#E6EDF3"
    TEXT_DIM = "#8B949E"
    BORDER = "#30363D"
    MSG_SELF = "#1F3A5F"
    MSG_OTHER = "#1C2333"
    SYSTEM_FG = "#F0883E"

    def __init__(self, master):

        self.master = master
        self.master.title("NeonChat")
        self.master.geometry("820x640")
        self.master.configure(bg=self.BG_DARK)

        self.nickname = None
        self.client = None
        self.running = False

        self.master.protocol("WM_DELETE_WINDOW", self.close)

        self.ask_nickname()

    def ask_nickname(self):

        dialog = tk.Toplevel(self.master)
        dialog.title("Join Chat")
        dialog.geometry("300x150")
        dialog.configure(bg=self.BG_DARK)

        tk.Label(dialog, text="Enter Nickname",
                 fg="white", bg=self.BG_DARK).pack(pady=10)

        entry = tk.Entry(dialog)
        entry.pack(pady=5)
        entry.focus()

        def submit():
            name = entry.get().strip()

            if not name:
                return

            self.nickname = name
            dialog.destroy()
            self.connect()

        tk.Button(dialog, text="Join", command=submit).pack(pady=10)

    def connect(self):

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((HOST, PORT))
            self.running = True

        except:
            messagebox.showerror("Error", "Cannot connect to server")
            self.master.destroy()
            return

        self.build_ui()

        thread = threading.Thread(target=self.receive)
        thread.daemon = True
        thread.start()

    def build_ui(self):

        self.text = tk.Text(self.master, bg=self.BG_DARK,
                            fg="white", state="disabled")
        self.text.pack(fill="both", expand=True, padx=10, pady=10)

        bottom = tk.Frame(self.master, bg=self.BG_MID)
        bottom.pack(fill="x")

        self.msg = tk.Entry(bottom)
        self.msg.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        self.msg.bind("<Return>", lambda e: self.send())

        send = tk.Button(bottom, text="Send", command=self.send)
        send.pack(side="right", padx=10)

    def add_message(self, message):

        self.text.configure(state="normal")
        self.text.insert("end", message + "\n")
        self.text.configure(state="disabled")
        self.text.see("end")

    def receive(self):

        while self.running:

            try:

                message = self.client.recv(BUFFER_SIZE).decode()

                if message == "NICK":
                    self.client.send(self.nickname.encode())

                else:
                    self.master.after(0, self.add_message, message)

            except:
                break

    def send(self):

        msg = self.msg.get().strip()

        if not msg:
            return

        time = datetime.now().strftime("%H:%M")
        full = f"[{time}] {self.nickname}: {msg}"

        try:
            self.client.send(full.encode())
        except:
            pass

        self.msg.delete(0, "end")

    def close(self):

        self.running = False

        try:
            self.client.close()
        except:
            pass

        self.master.destroy()


if __name__ == "__main__":

    root = tk.Tk()
    app = ModernChatApp(root)
    root.mainloop()
