import tkinter as tk
from tkinter import messagebox
from database import get_connection

# Colors
BG = "#f5f7fb"
SIDEBAR = "#101a2b"
BLUE = "#2563eb"
BLUE_DARK = "#1d4ed8"
WHITE = "#ffffff"
TEXT = "#111827"
GRAY = "#64748b"
BORDER = "#dbe2ea"

# Login Window
def show_login(show_register, open_main_window):
    login = tk.Tk()
    login.title("Product Demand Prediction System - Login")
    login.geometry("950x600")
    login.minsize(850, 550)
    login.configure(bg=BG)

    # Left Side - Project Information
    left = tk.Frame(
        login,
        bg=SIDEBAR,
        width=430
    )
    left.pack(side="left", fill="y")
    left.pack_propagate(False)

    tk.Label(
        left,
        text="PRODUCT",
        font=("Segoe UI", 30, "bold"),
        bg=SIDEBAR,
        fg=WHITE
    ).pack(pady=(120, 0))

    tk.Label(
        left,
        text="DEMAND PREDICTION",
        font=("Segoe UI", 18, "bold"),
        bg=SIDEBAR,
        fg="#93c5fd"
    ).pack(pady=(0, 25))

    tk.Label(
        left,
        text="Management System",
        font=("Segoe UI", 13),
        bg=SIDEBAR,
        fg="#cbd5e1"
    ).pack()

    tk.Label(
        left,
        text="\nMultiple Linear Regression\nfor Product Demand Prediction",
        font=("Segoe UI", 11),
        bg=SIDEBAR,
        fg="#94a3b8",
        justify="center"
    ).pack(pady=35)

    # Right Side - Login Form
    right = tk.Frame(login, bg=WHITE)
    right.pack(side="right", fill="both", expand=True)

    # Login Card
    card = tk.Frame(right, bg=WHITE)
    card.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    tk.Label(
        card,
        text="Welcome Back",
        font=("Segoe UI", 27, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack()

    tk.Label(
        card,
        text="Login to access your dashboard",
        font=("Segoe UI", 10),
        bg=WHITE,
        fg=GRAY
    ).pack(pady=(5, 25))

    # Username
    tk.Label(
        card,
        text="Username",
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(anchor="w")

    username_entry = tk.Entry(
        card,
        font=("Segoe UI", 11),
        width=32,
        bd=0,
        bg="#f8fafc",
        fg=TEXT,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    username_entry.pack(
        ipady=9,
        pady=(6, 15)
    )

    # Password
    tk.Label(
        card,
        text="Password",
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(anchor="w")

    password_entry = tk.Entry(
        card,
        font=("Segoe UI", 11),
        width=32,
        show="*",
        bd=0,
        bg="#f8fafc",
        fg=TEXT,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    password_entry.pack(
        ipady=9,
        pady=(6, 20)
    )

    # Login Function
    def login_user():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if username == "":
            messagebox.showwarning(
                "Login",
                "Please enter username."
            )
            username_entry.focus()
            return

        if password == "":
            messagebox.showwarning(
                "Login",
                "Please enter password."
            )
            password_entry.focus()
            return

        # Connect to database
        conn = get_connection()

        if conn is None:
            return

        try:
            cursor = conn.cursor()

            # Check username and password
            cursor.execute(
                "SELECT * FROM Users WHERE Username=%s AND Password=%s",
                (username, password)
            )

            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user:
                messagebox.showinfo(
                    "Login Successful",
                    "Welcome to Product Demand Prediction System!"
                )
                login.destroy()
                open_main_window()
            else:
                messagebox.showerror(
                    "Login Failed",
                    "Invalid username or password."
                )
                password_entry.delete(0, tk.END)
                password_entry.focus()

        except Exception as e:
            messagebox.showerror(
                "Login Error",
                str(e)
            )

    # Login Button
    tk.Button(
        card,
        text="LOGIN",
        command=login_user,
        font=("Segoe UI", 11, "bold"),
        bg=BLUE,
        fg=WHITE,
        activebackground=BLUE_DARK,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        width=30,
        pady=10
    ).pack(pady=(0, 15))

    # Register Button
    tk.Button(
        card,
        text="Don't have an account? Register",
        font=("Segoe UI", 9),
        bg=WHITE,
        fg=BLUE,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=lambda: go_to_register()
    ).pack()

    # Go to Register
    def go_to_register():
        login.destroy()
        show_register()

    # Press Enter to Login
    password_entry.bind(
        "<Return>",
        lambda event: login_user()
    )

    username_entry.focus()
    login.mainloop()
