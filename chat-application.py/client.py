import socket
import threading
import tkinter as tk
from tkinter import simpledialog
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

class ChatClient:

    def __init__(self, master):

        self.master = master
        master.title("Python Chat Application")

        self.chat_area = tk.Text(master)
        self.chat_area.pack(padx=20, pady=5)

        self.msg_entry = tk.Entry(master, width=50)
        self.msg_entry.pack(padx=20, pady=5)

        self.send_button = tk.Button(master, text="Send", command=self.write)
        self.send_button.pack(pady=5)

        self.nickname = simpledialog.askstring("Nickname", "Choose a nickname")

        self.running = True

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    def write(self):
        message = f"{self.nickname}: {self.msg_entry.get()}"
        timestamp = datetime.now().strftime("%H:%M")
        client.send(f"[{timestamp}] {message}".encode("utf-8"))
        self.msg_entry.delete(0, tk.END)

    def receive(self):
        while self.running:
            try:
                message = client.recv(1024).decode("utf-8")

                if message == "NICK":
                    client.send(self.nickname.encode("utf-8"))
                else:
                    self.chat_area.insert(tk.END, message + "\n")
                    self.chat_area.yview(tk.END)

            except:
                print("Error")
                client.close()
                break


root = tk.Tk()
gui = ChatClient(root)
root.mainloop()
