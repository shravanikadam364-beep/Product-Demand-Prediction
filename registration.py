import tkinter as tk
from tkinter import messagebox
from database import get_connection

# Colors
BG = "#f5f7fb"
SIDEBAR = "#101a2b"
BLUE = "#2563eb"
WHITE = "#ffffff"
TEXT = "#111827"
GRAY = "#64748b"
BORDER = "#dbe2ea"

# Register Window
def show_register(show_login):
    window = tk.Tk()
    window.title("Product Demand Prediction System - Register")
    window.geometry("900x600")
    window.configure(bg=BG)

    # Register Function
    def register():
        username = username_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        # Check username
        if username == "":
            messagebox.showerror("Error", "Please enter username")
            return

        # Check email
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Enter valid email")
            return

        # Check password
        if len(password) < 6:
            messagebox.showerror(
                "Error",
                "Password must be at least 6 characters"
            )
            return

        # Connect to database
        conn = get_connection()

        if conn is None:
            return

        try:
            cursor = conn.cursor()

            # Insert user into Users table
            cursor.execute(
                "INSERT INTO Users (Username, Email, Password) VALUES (%s, %s, %s)",
                (username, email, password)
            )

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Registration Successful!"
            )

            # Clear fields
            username_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Registration Error", str(e))

    # Left Side
    left_frame = tk.Frame(
        window,
        bg="#1f4e79",
        width=450,
        height=600
    )
    left_frame.pack(side="left", fill="both")
    left_frame.pack_propagate(False)

    # Project Title
    tk.Label(
        left_frame,
        text="PRODUCT DEMAND",
        font=("Arial", 25, "bold"),
        fg="white",
        bg="#1f4e79"
    ).pack(pady=(180, 5))

    tk.Label(
        left_frame,
        text="PREDICTION SYSTEM",
        font=("Arial", 25, "bold"),
        fg="white",
        bg="#1f4e79"
    ).pack()

    # Right Side
    right_frame = tk.Frame(
        window,
        bg="white",
        width=450,
        height=600
    )
    right_frame.pack(side="right", fill="both")
    right_frame.pack_propagate(False)

    # Registration Heading
    tk.Label(
        right_frame,
        text="Create Account",
        font=("Arial", 24, "bold"),
        bg="white",
        fg="#1f4e79"
    ).pack(pady=(70, 10))

    tk.Label(
        right_frame,
        text="Register to continue",
        font=("Arial", 11),
        bg="white",
        fg="gray"
    ).pack(pady=(0, 25))

    # Username
    tk.Label(
        right_frame,
        text="Username",
        font=("Arial", 11, "bold"),
        bg="white"
    ).pack(anchor="w", padx=70)

    username_entry = tk.Entry(
        right_frame,
        font=("Arial", 11),
        width=32
    )
    username_entry.pack(pady=(5, 15))

    # Email
    tk.Label(
        right_frame,
        text="Email",
        font=("Arial", 11, "bold"),
        bg="white"
    ).pack(anchor="w", padx=70)

    email_entry = tk.Entry(
        right_frame,
        font=("Arial", 11),
        width=32
    )
    email_entry.pack(pady=(5, 15))

    # Password
    tk.Label(
        right_frame,
        text="Password",
        font=("Arial", 11, "bold"),
        bg="white"
    ).pack(anchor="w", padx=70)

    password_entry = tk.Entry(
        right_frame,
        font=("Arial", 11),
        width=32,
        show="*"
    )
    password_entry.pack(pady=(5, 25))

    # Register Button
    tk.Button(
        right_frame,
        text="CREATE ACCOUNT",
        font=("Arial", 11, "bold"),
        bg="#1f4e79",
        fg="white",
        width=25,
        height=2,
        command=register
    ).pack()

    # Login Button
    tk.Button(
        right_frame,
        text="Already have an account? Login",
        font=("Arial", 10),
        bg="white",
        fg="#1f4e79",
        bd=0,
        cursor="hand2",
        command=lambda: go_to_login()
    ).pack(pady=20)

    # Go to Login
    def go_to_login():
        window.destroy()
        show_login()

    window.mainloop()
