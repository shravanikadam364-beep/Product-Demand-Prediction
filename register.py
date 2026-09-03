import tkinter as tk
from tkinter import messagebox
from database import get_connection

# Registration Page
def show_register(parent, success_callback):
    window = tk.Toplevel(parent)
    window.title("Product Demand Prediction System - Register")
    window.geometry("900x600")
    window.configure(bg="#eef2f7")
    window.resizable(False, False)

    # Close Registration Page
    def close_register():
        window.destroy()
        parent.deiconify()

    # Register Function
    def register():
        username = username_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        # Check Username
        if username == "":
            messagebox.showerror("Error", "Please enter username")
            username_entry.focus()
            return

        # Check Email
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Enter valid email")
            email_entry.focus()
            return

        # Check Password
        if len(password) < 6:
            messagebox.showerror(
                "Error",
                "Password must be at least 6 characters"
            )
            password_entry.focus()
            return

        # Connect Database
        conn = get_connection()

        if conn is None:
            return

        try:
            cursor = conn.cursor()

            # Insert User Data
            cursor.execute(
                "INSERT INTO Users (Username, Email, Password) VALUES (%s, %s, %s)",
                (username, email, password)
            )

            conn.commit()

            cursor.close()
            conn.close()

            # Registration Successful
            messagebox.showinfo(
                "Success",
                "Registration Successful!\nYou can now login."
            )

            # Close Registration and Open Dashboard
            window.destroy()
            parent.destroy()
            success_callback()

        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()

            # Duplicate Username or Email
            if "Duplicate entry" in str(e):
                messagebox.showerror(
                    "Registration Error",
                    "Username or Email already exists."
                )
            else:
                messagebox.showerror(
                    "Registration Error",
                    str(e)
                )

    # ==============================
    # LEFT SIDE
    # ==============================

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

    tk.Label(
        left_frame,
        text="Multiple Linear Regression",
        font=("Arial", 11),
        fg="#dbeafe",
        bg="#1f4e79"
    ).pack(pady=20)

    # ==============================
    # RIGHT SIDE
    # ==============================

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
    ).pack(pady=(60, 10))

    tk.Label(
        right_frame,
        text="Register to continue",
        font=("Arial", 11),
        bg="white",
        fg="gray"
    ).pack(pady=(0, 25))

    # ==============================
    # USERNAME
    # ==============================

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

    # ==============================
    # EMAIL
    # ==============================

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

    # ==============================
    # PASSWORD
    # ==============================

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

    # ==============================
    # REGISTER BUTTON
    # ==============================

    tk.Button(
        right_frame,
        text="CREATE ACCOUNT",
        font=("Arial", 11, "bold"),
        bg="#1f4e79",
        fg="white",
        width=25,
        height=2,
        relief="flat",
        cursor="hand2",
        command=register
    ).pack()

    # Login Information
    tk.Label(
        right_frame,
        text="Already have an account? Go back to Login",
        font=("Arial", 10),
        bg="white",
        fg="#1f4e79"
    ).pack(pady=20)

    # Window Close
    window.protocol("WM_DELETE_WINDOW", close_register)

    username_entry.focus()
