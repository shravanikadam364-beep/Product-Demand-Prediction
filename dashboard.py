import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from database import get_connection

# COLORS
BG = "#f5f7fb"
SIDEBAR = "#101a2b"
CARD_BLUE = "#2563eb"
CARD_GREEN = "#16a34a"
CARD_PURPLE = "#7c3aed"
CARD_ORANGE = "#f97316"
WHITE = "#ffffff"
TEXT = "#111827"
GRAY = "#64748b"
BORDER = "#dbe2ea"

# SHOW DASHBOARD
def show_dashboard(content, show_page):
    # Clear previous page
    for widget in content.winfo_children():
        widget.destroy()

    content.configure(bg=BG)

    # HEADER
    header = tk.Frame(
        content,
        bg=BG
    )
    header.pack(
        fill="x",
        pady=(25, 5)
    )

    tk.Label(
        header,
        text="Dashboard",
        font=("Segoe UI", 30, "bold"),
        bg=BG,
        fg=TEXT
    ).pack()

    tk.Label(
        header,
        text="Product Demand Prediction System",
        font=("Segoe UI", 12),
        bg=BG,
        fg=GRAY
    ).pack(pady=(2, 0))

    # Small blue line
    tk.Frame(
        header,
        bg=CARD_BLUE,
        height=3,
        width=90
    ).pack(pady=12)

    # GET DATABASE COUNTS
    total_products = 0
    total_sales = 0
    total_predictions = 0
    total_demand = 0.0

    try:
        conn = get_connection()

        if conn:
            cursor = conn.cursor()

            # Products
            cursor.execute(
                "SELECT COUNT(*) FROM Product"
            )
            total_products = cursor.fetchone()[0]

            # Sales
            cursor.execute(
                "SELECT COUNT(*) FROM Sales"
            )
            total_sales = cursor.fetchone()[0]

            # Predictions
            cursor.execute(
                "SELECT COUNT(*) FROM Demand_Prediction"
            )
            total_predictions = cursor.fetchone()[0]

            # Total predicted demand
            cursor.execute("""
                SELECT COALESCE(
                    SUM(Predicted_Demand),
                    0
                )
                FROM Demand_Prediction
            """)

            total_demand = cursor.fetchone()[0]

            cursor.close()
            conn.close()

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )

    # STATISTICS FRAME
    cards_frame = tk.Frame(
        content,
        bg=BG
    )

    cards_frame.pack(
        fill="x",
        padx=45,
        pady=12
    )

    cards_frame.columnconfigure(0, weight=1)
    cards_frame.columnconfigure(1, weight=1)
    cards_frame.columnconfigure(2, weight=1)
    cards_frame.columnconfigure(3, weight=1)

    # CARD FUNCTION
    def create_card(
        parent,
        column,
        title,
        value,
        color,
        button_text,
        command,
        suffix=""
    ):
        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            padx=8,
            sticky="nsew"
        )

        # Top color line
        tk.Frame(
            card,
            bg=color,
            height=5
        ).pack(fill="x")

        # Content
        inner = tk.Frame(
            card,
            bg=WHITE,
            padx=15,
            pady=15
        )

        inner.pack(
            fill="both",
            expand=True
        )

        # Icon circle
        icon = tk.Canvas(
            inner,
            width=52,
            height=52,
            bg=WHITE,
            highlightthickness=0
        )

        icon.pack(pady=(0, 8))

        icon.create_oval(
            5,
            5,
            47,
            47,
            fill=color,
            outline=color
        )

        icon.create_text(
            26,
            26,
            text="●",
            fill=WHITE,
            font=("Segoe UI", 15, "bold")
        )

        # Title
        tk.Label(
            inner,
            text=title,
            font=("Segoe UI", 11, "bold"),
            bg=WHITE,
            fg=GRAY
        ).pack()

        # Value
        tk.Label(
            inner,
            text=str(value),
            font=("Segoe UI", 25, "bold"),
            bg=WHITE,
            fg=color
        ).pack(pady=(7, 2))

        # Suffix
        if suffix:
            tk.Label(
                inner,
                text=suffix,
                font=("Segoe UI", 10, "bold"),
                bg=WHITE,
                fg=color
            ).pack()

        # View button
        tk.Button(
            inner,
            text=button_text,
            command=command,
            font=("Segoe UI", 9, "bold"),
            bg=color,
            fg=WHITE,
            activebackground=color,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=18,
            pady=6
        ).pack(pady=(12, 0))

    # CREATE FOUR CARDS
    create_card(
        cards_frame,
        0,
        "TOTAL PRODUCTS",
        total_products,
        CARD_BLUE,
        "View Details",
        lambda: show_page("products")
    )

    create_card(
        cards_frame,
        1,
        "TOTAL SALES",
        total_sales,
        CARD_GREEN,
        "View Details",
        lambda: show_page("sales")
    )

    create_card(
        cards_frame,
        2,
        "TOTAL PREDICTIONS",
        total_predictions,
        CARD_PURPLE,
        "View Details",
        lambda: show_page("prediction")
    )

    create_card(
        cards_frame,
        3,
        "TOTAL PREDICTED DEMAND",
        f"{float(total_demand):.2f}",
        CARD_ORANGE,
        "View Details",
        lambda: show_page("reports"),
        "Units"
    )

    # MACHINE LEARNING SECTION
    ml_frame = tk.Frame(
        content,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    ml_frame.pack(
        fill="x",
        padx=45,
        pady=(20, 10)
    )

    # ML heading
    tk.Label(
        ml_frame,
        text="Machine Learning Model",
        font=("Segoe UI", 19, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=30,
        pady=(20, 5)
    )

    tk.Frame(
        ml_frame,
        bg=CARD_BLUE,
        height=3,
        width=55
    ).pack(
        anchor="w",
        padx=30,
        pady=(0, 15)
    )

    # ML content
    ml_content = tk.Frame(
        ml_frame,
        bg=WHITE
    )

    ml_content.pack(
        fill="x",
        padx=30,
        pady=(0, 20)
    )

    # Description
    description = tk.Frame(
        ml_content,
        bg=WHITE
    )

    description.grid(
        row=0,
        column=0,
        padx=(0, 50),
        sticky="w"
    )

    tk.Label(
        description,
        text="Multiple Linear Regression",
        font=("Segoe UI", 14, "bold"),
        bg=WHITE,
        fg=CARD_BLUE
    ).pack(anchor="w")

    tk.Label(
        description,
        text=(
            "Multiple Linear Regression is used to predict\n"
            "product demand based on important sales factors."
        ),
        font=("Segoe UI", 10),
        bg=WHITE,
        fg=GRAY,
        justify="left"
    ).pack(
        anchor="w",
        pady=(7, 0)
    )

    # INPUT FACTORS
    factors = tk.Frame(
        ml_content,
        bg=WHITE
    )

    factors.grid(
        row=0,
        column=1,
        padx=30
    )

    tk.Label(
        factors,
        text="✓  Price",
        font=("Segoe UI", 11),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w",
        pady=3
    )

    tk.Label(
        factors,
        text="✓  Discount",
        font=("Segoe UI", 11),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w",
        pady=3
    )

    tk.Label(
        factors,
        text="✓  Previous Sales",
        font=("Segoe UI", 11),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w",
        pady=3
    )

    # PREDICTED DEMAND BOX
    prediction_box = tk.Frame(
        ml_content,
        bg="#eef4ff",
        highlightbackground="#cbdcfb",
        highlightthickness=1,
        padx=30,
        pady=18
    )

    prediction_box.grid(
        row=0,
        column=2,
        padx=20
    )

    tk.Label(
        prediction_box,
        text="Predicted Demand",
        font=("Segoe UI", 13, "bold"),
        bg="#eef4ff",
        fg=TEXT
    ).pack()

    tk.Label(
        prediction_box,
        text="Price + Discount + Previous Sales",
        font=("Segoe UI", 9),
        bg="#eef4ff",
        fg=GRAY
    ).pack(pady=(5, 0))

    # INVENTORY MESSAGE
    message = tk.Frame(
        ml_frame,
        bg="#eef4ff",
        padx=20,
        pady=10
    )

    message.pack(
        fill="x",
        padx=30,
        pady=(0, 20)
    )

    tk.Label(
        message,
        text=(
            "★  Accurate demand predictions help in better "
            "inventory planning and decision making."
        ),
        font=("Segoe UI", 10),
        bg="#eef4ff",
        fg="#1e40af"
    ).pack()

    # FOOTER INFORMATION
    footer = tk.Frame(
        content,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    footer.pack(
        fill="x",
        padx=45,
        pady=(5, 20)
    )

    now = datetime.now()

    # Date
    date_frame = tk.Frame(
        footer,
        bg=WHITE
    )

    date_frame.pack(
        side="left",
        expand=True,
        pady=15
    )

    tk.Label(
        date_frame,
        text="System Date",
        font=("Segoe UI", 9),
        bg=WHITE,
        fg=CARD_BLUE
    ).pack()

    tk.Label(
        date_frame,
        text=now.strftime("%d %B %Y"),
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack()

    # Time
    time_frame = tk.Frame(
        footer,
        bg=WHITE
    )

    time_frame.pack(
        side="left",
        expand=True,
        pady=15
    )

    tk.Label(
        time_frame,
        text="System Time",
        font=("Segoe UI", 9),
        bg=WHITE,
        fg=CARD_BLUE
    ).pack()

    tk.Label(
        time_frame,
        text=now.strftime("%I:%M:%S %p"),
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack()

    # Welcome
    welcome_frame = tk.Frame(
        footer,
        bg=WHITE
    )

    welcome_frame.pack(
        side="left",
        expand=True,
        pady=15
    )

    tk.Label(
        welcome_frame,
        text="Welcome",
        font=("Segoe UI", 9),
        bg=WHITE,
        fg=CARD_BLUE
    ).pack()

    tk.Label(
        welcome_frame,
        text="Admin",
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack()
