import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
import re

HOST = "127.0.0.1"
PORT = 5555


class ModernChatApp:
    # ── Color palette ──────────────────────────────────────────
    BG_DARK    = "#0D1117"
    BG_MID     = "#161B22"
    BG_CARD    = "#1C2333"
    ACCENT     = "#58A6FF"
    ACCENT2    = "#3FB950"
    TEXT_MAIN  = "#E6EDF3"
    TEXT_DIM   = "#8B949E"
    BORDER     = "#30363D"
    MSG_SELF   = "#1F3A5F"
    MSG_OTHER  = "#1C2333"
    SYSTEM_FG  = "#F0883E"
    BUBBLE_RAD = 14

    def __init__(self, master):
        self.master = master
        self.master.title("NeonChat")
        self.master.geometry("820x640")
        self.master.minsize(600, 480)
        self.master.configure(bg=self.BG_DARK)
        self.master.resizable(True, True)

        self.nickname = None
        self.client   = None
        self.running  = False
        self.online_users: list[str] = []

        # Custom font fallback chain
        self._fonts = {
            "title":   ("Segoe UI", 18, "bold"),
            "sub":     ("Segoe UI", 10),
            "msg":     ("Segoe UI", 11),
            "time":    ("Segoe UI", 8),
            "input":   ("Segoe UI", 12),
            "btn":     ("Segoe UI", 11, "bold"),
            "nick":    ("Segoe UI", 11, "bold"),
            "online":  ("Segoe UI", 10),
            "header":  ("Segoe UI", 10, "bold"),
        }

        self._ask_nickname()

    # ── Step 1: ask for nickname before building UI ─────────────
    def _ask_nickname(self):
        dlg = NicknameDialog(self.master)
        self.master.wait_window(dlg.top)
        if not dlg.result:
            self.master.destroy()
            return
        self.nickname = dlg.result.strip()[:20] or "User"
        self._connect()

    # ── Step 2: connect to server ───────────────────────────────
    def _connect(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((HOST, PORT))
            self.running = True
        except ConnectionRefusedError:
            messagebox.showerror(
                "Connection Failed",
                f"Could not connect to {HOST}:{PORT}\n\nMake sure server.py is running first."
            )
            self.master.destroy()
            return

        self._build_ui()

        t = threading.Thread(target=self._receive_loop, daemon=True)
        t.start()

    # ── Build the full UI ───────────────────────────────────────
    def _build_ui(self):
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=0)
        self.master.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_chat_area()
        self._build_sidebar()
        self._build_input_bar()
        self._build_status_bar()

    def _build_header(self):
        hdr = tk.Frame(self.master, bg=self.BG_MID, height=56)
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew")
        hdr.grid_propagate(False)

        # Coloured dot
        dot = tk.Canvas(hdr, width=12, height=12, bg=self.BG_MID,
                        highlightthickness=0)
        dot.place(x=20, y=22)
        dot.create_oval(0, 0, 12, 12, fill=self.ACCENT2, outline="")

        tk.Label(
            hdr, text="NeonChat", font=self._fonts["title"],
            fg=self.ACCENT, bg=self.BG_MID
        ).place(x=40, y=10)

        self.status_label = tk.Label(
            hdr, text=f"● Connected as  {self.nickname}",
            font=self._fonts["sub"], fg=self.ACCENT2, bg=self.BG_MID
        )
        self.status_label.place(relx=1.0, x=-20, y=18, anchor="e")

        sep = tk.Frame(self.master, bg=self.BORDER, height=1)
        sep.grid(row=0, column=0, columnspan=2, sticky="sew")

    def _build_chat_area(self):
        outer = tk.Frame(self.master, bg=self.BG_DARK)
        outer.grid(row=1, column=0, sticky="nsew", padx=(12, 4), pady=8)
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            outer, bg=self.BG_DARK, highlightthickness=0,
            bd=0, cursor="arrow"
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        sb = tk.Scrollbar(outer, orient="vertical", command=self.canvas.yview,
                          bg=self.BG_MID, troughcolor=self.BG_DARK,
                          activebackground=self.ACCENT, width=8)
        sb.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=sb.set)

        self.msg_frame = tk.Frame(self.canvas, bg=self.BG_DARK)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.msg_frame, anchor="nw"
        )

        self.msg_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _build_sidebar(self):
        side = tk.Frame(self.master, bg=self.BG_MID, width=180)
        side.grid(row=1, column=1, sticky="nsew", padx=(0, 12), pady=8)
        side.grid_propagate(False)

        tk.Label(
            side, text="ONLINE", font=self._fonts["header"],
            fg=self.TEXT_DIM, bg=self.BG_MID
        ).pack(anchor="w", padx=14, pady=(14, 6))

        tk.Frame(side, bg=self.BORDER, height=1).pack(fill="x", padx=10)

        self.users_frame = tk.Frame(side, bg=self.BG_MID)
        self.users_frame.pack(fill="both", expand=True, padx=4, pady=4)

    def _build_input_bar(self):
        bar = tk.Frame(self.master, bg=self.BG_MID, height=64)
        bar.grid(row=2, column=0, columnspan=2, sticky="ew",
                 padx=12, pady=(0, 6))
        bar.grid_propagate(False)
        bar.grid_columnconfigure(0, weight=1)

        entry_bg = tk.Frame(bar, bg=self.BORDER, bd=0)
        entry_bg.grid(row=0, column=0, sticky="ew", padx=(10, 8), pady=12,
                      ipady=1)
        entry_bg.grid_columnconfigure(0, weight=1)

        self.msg_var = tk.StringVar()
        self.entry = tk.Entry(
            entry_bg, textvariable=self.msg_var,
            font=self._fonts["input"], bg=self.BG_CARD,
            fg=self.TEXT_MAIN, insertbackground=self.ACCENT,
            relief="flat", bd=8,
            highlightthickness=1, highlightcolor=self.ACCENT,
            highlightbackground=self.BORDER
        )
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", lambda e: self._send_message())
        self.entry.focus()

        send_btn = tk.Button(
            bar, text="Send ➤",
            font=self._fonts["btn"],
            bg=self.ACCENT, fg=self.BG_DARK,
            activebackground="#3A8BE0", activeforeground=self.BG_DARK,
            relief="flat", bd=0, padx=18, pady=6,
            cursor="hand2", command=self._send_message
        )
        send_btn.grid(row=0, column=1, padx=(0, 10), pady=10)

    def _build_status_bar(self):
        sb = tk.Frame(self.master, bg=self.BG_MID, height=22)
        sb.grid(row=3, column=0, columnspan=2, sticky="ew")
        sb.grid_propagate(False)

        self.footer_label = tk.Label(
            sb, text=f"🔒 Encrypted  |  {HOST}:{PORT}",
            font=("Segoe UI", 8), fg=self.TEXT_DIM, bg=self.BG_MID
        )
        self.footer_label.pack(side="right", padx=12)

    # ── Message rendering ───────────────────────────────────────
    def _add_message(self, raw: str):
        """Parse and render a single message bubble."""
        # SYSTEM messages
        if raw.startswith("SYSTEM:"):
            text = raw[7:]
            lbl = tk.Label(
                self.msg_frame, text=f"— {text} —",
                font=("Segoe UI", 9, "italic"),
                fg=self.SYSTEM_FG, bg=self.BG_DARK,
                wraplength=480
            )
            lbl.pack(anchor="center", pady=4)
            self._scroll_bottom()
            return

        # Normal message: "[HH:MM] Nickname: body"
        is_self = False
        time_str = ""
        nick = ""
        body = raw

        match = re.match(r"^\[(\d{2}:\d{2})\]\s*(.+?):\s*(.*)", raw, re.DOTALL)
        if match:
            time_str = match.group(1)
            nick  = match.group(2)
            body  = match.group(3)
            is_self = (nick == self.nickname)

        anchor   = "e" if is_self else "w"
        padx     = (80, 12) if is_self else (12, 80)
        bg_color = self.MSG_SELF if is_self else self.MSG_OTHER
        nick_col = self.ACCENT if is_self else self.ACCENT2

        row = tk.Frame(self.msg_frame, bg=self.BG_DARK)
        row.pack(fill="x", anchor=anchor, padx=padx, pady=3)

        bubble = tk.Frame(row, bg=bg_color, bd=0)
        bubble.pack(anchor=anchor)

        if nick and not is_self:
            tk.Label(
                bubble, text=nick,
                font=self._fonts["nick"], fg=nick_col, bg=bg_color
            ).pack(anchor="w", padx=10, pady=(6, 0))

        tk.Label(
            bubble, text=body,
            font=self._fonts["msg"], fg=self.TEXT_MAIN, bg=bg_color,
            wraplength=420, justify="left"
        ).pack(anchor="w", padx=10, pady=(2, 2))

        if time_str:
            tk.Label(
                bubble, text=time_str,
                font=self._fonts["time"], fg=self.TEXT_DIM, bg=bg_color
            ).pack(anchor="e", padx=10, pady=(0, 6))

        self._scroll_bottom()

    def _update_users(self, csv_names: str):
        for w in self.users_frame.winfo_children():
            w.destroy()
        self.online_users = [n for n in csv_names.split(",") if n]
        for name in self.online_users:
            row = tk.Frame(self.users_frame, bg=self.BG_MID)
            row.pack(fill="x", pady=2, padx=6)

            dot = tk.Canvas(row, width=8, height=8, bg=self.BG_MID,
                            highlightthickness=0)
            dot.pack(side="left", padx=(4, 6), pady=8)
            color = self.ACCENT if name == self.nickname else self.ACCENT2
            dot.create_oval(0, 0, 8, 8, fill=color, outline="")

            tk.Label(
                row, text=name,
                font=self._fonts["online"],
                fg=self.TEXT_MAIN if name == self.nickname else self.TEXT_DIM,
                bg=self.BG_MID
            ).pack(side="left")

        self.footer_label.config(
            text=f"🔒 Encrypted  |  {HOST}:{PORT}  |  {len(self.online_users)} online"
        )

    # ── Network ─────────────────────────────────────────────────
    def _receive_loop(self):
        while self.running:
            try:
                raw = self.client.recv(2048).decode("utf-8")
                if not raw:
                    break

                if raw == "NICK":
                    self.client.send(self.nickname.encode("utf-8"))

                elif raw.startswith("USERS:"):
                    csv = raw[6:]
                    self.master.after(0, self._update_users, csv)

                elif raw.startswith("SYSTEM:"):
                    # After someone joins/leaves re-request user list
                    self.master.after(0, self._add_message, raw)

                else:
                    self.master.after(0, self._add_message, raw)

            except Exception as e:
                if self.running:
                    self.master.after(0, self._add_message,
                                      "SYSTEM:Disconnected from server.")
                self.running = False
                break

    def _send_message(self):
        text = self.msg_var.get().strip()
        if not text:
            return
        timestamp = datetime.now().strftime("%H:%M")
        full = f"[{timestamp}] {self.nickname}: {text}"
        try:
            self.client.send(full.encode("utf-8"))
        except:
            self._add_message("SYSTEM:Failed to send — not connected.")
        self.msg_var.set("")

    # ── Canvas helpers ──────────────────────────────────────────
    def _on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _scroll_bottom(self):
        self.master.after(50, lambda: self.canvas.yview_moveto(1.0))


# ── Custom nickname dialog ───────────────────────────────────────
class NicknameDialog:
    BG      = "#0D1117"
    BG_CARD = "#1C2333"
    ACCENT  = "#58A6FF"
    TEXT    = "#E6EDF3"
    DIM     = "#8B949E"
    BORDER  = "#30363D"

    def __init__(self, parent):
        self.result = None
        self.top = tk.Toplevel(parent)
        self.top.title("Join NeonChat")
        self.top.geometry("380x260")
        self.top.resizable(False, False)
        self.top.configure(bg=self.BG)
        self.top.grab_set()

        # Center over parent
        parent.update_idletasks()
        px = parent.winfo_x() + (parent.winfo_width()  - 380) // 2
        py = parent.winfo_y() + (parent.winfo_height() - 260) // 2
        self.top.geometry(f"+{px}+{py}")

        # Header
        tk.Label(
            self.top, text="NeonChat", font=("Segoe UI", 22, "bold"),
            fg=self.ACCENT, bg=self.BG
        ).pack(pady=(30, 4))

        tk.Label(
            self.top, text="Choose your nickname to enter the chat",
            font=("Segoe UI", 10), fg=self.DIM, bg=self.BG
        ).pack()

        # Entry
        ef = tk.Frame(self.top, bg=self.BORDER, bd=0)
        ef.pack(padx=40, pady=18, fill="x")

        self.nick_var = tk.StringVar()
        e = tk.Entry(
            ef, textvariable=self.nick_var,
            font=("Segoe UI", 13), bg=self.BG_CARD,
            fg=self.TEXT, insertbackground=self.ACCENT,
            relief="flat", bd=10,
            highlightthickness=1, highlightcolor=self.ACCENT,
            highlightbackground=self.BORDER
        )
        e.pack(fill="x")
        e.focus()
        e.bind("<Return>", lambda ev: self._ok())

        # Button
        tk.Button(
            self.top, text="Enter Chat →",
            font=("Segoe UI", 11, "bold"),
            bg=self.ACCENT, fg=self.BG,
            activebackground="#3A8BE0", activeforeground=self.BG,
            relief="flat", bd=0, padx=24, pady=8,
            cursor="hand2", command=self._ok
        ).pack()

    def _ok(self):
        val = self.nick_var.get().strip()
        if val:
            self.result = val
            self.top.destroy()
        else:
            self.nick_var.set("")


# ── Entry point ─────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()          # hide until nickname is chosen
    app = ModernChatApp(root)
    root.deiconify()
    root.mainloop()
