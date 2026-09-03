import tkinter as tk
from tkinter import messagebox
from database import get_connection
from dashboard import show_dashboard
from products import show_products
from sales import show_sales
from prediction import show_prediction
from graphs import show_graph
from reports import show_reports
from register import show_register
from history import show_history


# COLORS

SIDEBAR_COLOR = "#111827"
SIDEBAR_BUTTON = "#1f2937"
SIDEBAR_ACTIVE = "#2563eb"
BG_COLOR = "#f4f6f9"
WHITE = "#ffffff"
TEXT_COLOR = "#111827"

# LOGIN WINDOW


def show_login():
    login = tk.Tk()
    login.title("Product Demand Prediction System - Login")
    login.geometry("950x600")
    login.minsize(850, 550)
    login.configure(bg=BG_COLOR)

    # ==============================
    # LEFT PANEL
    # ==============================

    left = tk.Frame(login, bg=SIDEBAR_COLOR, width=430)
    left.pack(side="left", fill="y")
    left.pack_propagate(False)

    # Project Title
    tk.Label(
        left,
        text="PRODUCT",
        font=("Segoe UI", 30, "bold"),
        bg=SIDEBAR_COLOR,
        fg=WHITE
    ).pack(pady=(120, 0))

    tk.Label(
        left,
        text="DEMAND PREDICTION",
        font=("Segoe UI", 18, "bold"),
        bg=SIDEBAR_COLOR,
        fg="#93c5fd"
    ).pack(pady=(0, 20))

    tk.Label(
        left,
        text="System",
        font=("Segoe UI", 13),
        bg=SIDEBAR_COLOR,
        fg="#cbd5e1"
    ).pack()

    tk.Label(
        left,
        text="\nMultiple Linear Regression\nfor Product Demand Prediction",
        font=("Segoe UI", 11),
        bg=SIDEBAR_COLOR,
        fg="#94a3b8",
        justify="center"
    ).pack(pady=30)

    # ==============================
    # RIGHT PANEL
    # ==============================

    right = tk.Frame(login, bg=WHITE)
    right.pack(side="right", fill="both", expand=True)

    # Login Card
    card = tk.Frame(right, bg=WHITE)
    card.place(relx=0.5, rely=0.5, anchor="center")

    # Login Heading
    tk.Label(
        card,
        text="Welcome Back",
        font=("Segoe UI", 27, "bold"),
        bg=WHITE,
        fg=TEXT_COLOR
    ).pack()

    tk.Label(
        card,
        text="Login to access your dashboard",
        font=("Segoe UI", 10),
        bg=WHITE,
        fg="#64748b"
    ).pack(pady=(5, 25))

    # ==============================
    # USERNAME
    # ==============================

    tk.Label(
        card,
        text="Username",
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=TEXT_COLOR
    ).pack(anchor="w")

    username_entry = tk.Entry(
        card,
        font=("Segoe UI", 11),
        width=32,
        bd=0,
        bg="#f8fafc",
        fg=TEXT_COLOR,
        highlightbackground="#dbe2ea",
        highlightthickness=1
    )
    username_entry.pack(ipady=9, pady=(6, 15))

    # ==============================
    # PASSWORD
    # ==============================

    tk.Label(
        card,
        text="Password",
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=TEXT_COLOR
    ).pack(anchor="w")

    password_entry = tk.Entry(
        card,
        font=("Segoe UI", 11),
        width=32,
        show="*",
        bd=0,
        bg="#f8fafc",
        fg=TEXT_COLOR,
        highlightbackground="#dbe2ea",
        highlightthickness=1
    )
    password_entry.pack(ipady=9, pady=(6, 20))

    # ==============================
    # LOGIN FUNCTION
    # ==============================

    def login_user():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        # Check Username
        if username == "":
            messagebox.showwarning(
                "Login",
                "Please enter username."
            )
            username_entry.focus()
            return

        # Check Password
        if password == "":
            messagebox.showwarning(
                "Login",
                "Please enter password."
            )
            password_entry.focus()
            return

        # Connect Database
        conn = get_connection()

        if conn is None:
            return

        try:
            cursor = conn.cursor()

            # Check Login Details
            cursor.execute(
                "SELECT * FROM Users WHERE Username=%s AND Password=%s",
                (username, password)
            )

            user = cursor.fetchone()

            cursor.close()
            conn.close()

            # Successful Login
            if user:
                messagebox.showinfo(
                    "Login Successful",
                    "Welcome to Product Demand Prediction System!"
                )
                login.destroy()
                create_main_window()

            # Failed Login
            else:
                messagebox.showerror(
                    "Login Failed",
                    "Invalid username or password."
                )
                password_entry.delete(0, tk.END)
                password_entry.focus()

        except Exception as e:
            conn.close()
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # ==============================
    # LOGIN BUTTON
    # ==============================

    tk.Button(
        card,
        text="LOGIN",
        command=login_user,
        font=("Segoe UI", 11, "bold"),
        bg="#2563eb",
        fg=WHITE,
        activebackground="#1d4ed8",
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        width=30,
        pady=10
    ).pack(pady=(0, 10))

    # ==============================
    # REGISTRATION FUNCTION
    # ==============================

    def open_registration():
        login.withdraw()
        show_register(login, create_main_window)

    # ==============================
    # REGISTER BUTTON
    # ==============================

    tk.Button(
        card,
        text="CREATE NEW ACCOUNT",
        command=open_registration,
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg="#2563eb",
        activebackground=WHITE,
        activeforeground="#1d4ed8",
        relief="flat",
        bd=0,
        cursor="hand2"
    ).pack(pady=(0, 8))

    # Registration Information
    tk.Label(
        card,
        text="Register a new account to login",
        font=("Segoe UI", 9),
        bg=WHITE,
        fg="#64748b"
    ).pack()

    # Enter Key Login
    password_entry.bind(
        "<Return>",
        lambda event: login_user()
    )

    username_entry.focus()
    login.mainloop()

# ==============================
# MAIN APPLICATION WINDOW
# ==============================

def create_main_window():
    root = tk.Tk()
    root.title("Product Demand Prediction System")
    root.geometry("1200x700")
    root.minsize(1000, 600)
    root.configure(bg=BG_COLOR)

    # ==============================
    # SIDEBAR
    # ==============================

    sidebar = tk.Frame(
        root,
        bg=SIDEBAR_COLOR,
        width=230
    )
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # Logo
    tk.Label(
        sidebar,
        text="PRODUCT",
        font=("Segoe UI", 18, "bold"),
        bg=SIDEBAR_COLOR,
        fg=WHITE
    ).pack(pady=(30, 0))

    tk.Label(
        sidebar,
        text="DEMAND SYSTEM",
        font=("Segoe UI", 10, "bold"),
        bg=SIDEBAR_COLOR,
        fg="#9ca3af"
    ).pack(pady=(0, 30))

    # ==============================
    # CONTENT AREA
    # ==============================

    content = tk.Frame(root, bg=BG_COLOR)
    content.pack(side="right", fill="both", expand=True)

    # ==============================
    # PAGE FUNCTION
    # ==============================

    def show_page(page):
        # Clear Previous Page
        for widget in content.winfo_children():
            widget.destroy()

        # Dashboard
        if page == "dashboard":
            show_dashboard(content, show_page)

        # Products
        elif page == "products":
            show_products(content)

        # Sales
        elif page == "sales":
            show_sales(content)

        # Demand Prediction
        elif page == "prediction":
            show_prediction(content)

        # Graph
        elif page == "graph":
            show_graph(content)

        # Reports
        elif page == "reports":
            show_reports(content)

        # History
        elif page == "history":
            show_history(content)

    # ==============================
    # MENU BUTTON FUNCTION
    # ==============================

    def create_menu_button(text, page):
        tk.Button(
            sidebar,
            text=text,
            font=("Segoe UI", 11, "bold"),
            bg=SIDEBAR_BUTTON,
            fg=WHITE,
            activebackground=SIDEBAR_ACTIVE,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            anchor="w",
            padx=25,
            pady=12,
            command=lambda: show_page(page)
        ).pack(
            fill="x",
            padx=12,
            pady=4
        )

    # ==============================
    # MENU BUTTONS
    # ==============================

    create_menu_button("🏠  Dashboard", "dashboard")
    create_menu_button("📦  Products", "products")
    create_menu_button("🛒  Sales", "sales")
    create_menu_button("🤖  Demand Prediction", "prediction")
    create_menu_button("📈  Graph", "graph")
    create_menu_button("📋  Reports", "reports")
    create_menu_button("🕒  History", "history")

    # ==============================
    # LOGOUT FUNCTION
    # ==============================

    def logout():
        answer = messagebox.askyesno(
            "Logout",
            "Do you want to logout?"
        )

        if answer:
            root.destroy()
            show_login()

    # ==============================
    # LOGOUT BUTTON
    # ==============================

    tk.Button(
        sidebar,
        text="🚪  Logout",
        font=("Segoe UI", 11, "bold"),
        bg="#991b1b",
        fg=WHITE,
        activebackground="#7f1d1d",
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        anchor="w",
        padx=25,
        pady=12,
        command=logout
    ).pack(
        side="bottom",
        fill="x",
        padx=12,
        pady=20
    )

    # ==============================
    # OPEN DASHBOARD
    # ==============================

    show_page("dashboard")
    root.mainloop()

# ==============================
# START PROGRAM
# ==============================

if __name__ == "__main__":
    show_login()
