import tkinter as tk
from tkinter import messagebox
from database import get_connection

# ==============================
# COLORS
# ==============================

BG_COLOR = "#f4f6f9"
WHITE = "#ffffff"
TEXT_COLOR = "#111827"
SUBTEXT = "#64748b"
BLUE = "#2563eb"
BORDER = "#dbe2ea"

# ==============================
# SHOW HISTORY
# ==============================

def show_history(content):
    # Clear Previous Page
    for widget in content.winfo_children():
        widget.destroy()

    content.configure(bg=BG_COLOR)

    # ==============================
    # PAGE HEADER
    # ==============================

    tk.Label(
        content,
        text="Prediction History",
        font=("Segoe UI", 27, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=(25, 5))

    tk.Label(
        content,
        text="Previous Product Demand Predictions",
        font=("Segoe UI", 11),
        bg=BG_COLOR,
        fg=SUBTEXT
    ).pack(pady=(0, 20))

    # ==============================
    # TABLE FRAME
    # ==============================

    table_frame = tk.Frame(
        content,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    table_frame.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=10
    )

    # ==============================
    # TABLE HEADINGS
    # ==============================

    headings = [
        "Prediction ID",
        "Product ID",
        "Price",
        "Discount",
        "Previous Sales",
        "Predicted Demand"
    ]

    for column, heading in enumerate(headings):
        tk.Label(
            table_frame,
            text=heading,
            font=("Segoe UI", 10, "bold"),
            bg=BLUE,
            fg=WHITE,
            padx=10,
            pady=12
        ).grid(
            row=0,
            column=column,
            sticky="nsew"
        )

    # ==============================
    # GET HISTORY FROM DATABASE
    # ==============================

    conn = get_connection()

    if conn is None:
        return

    try:
        cursor = conn.cursor()

        # Get prediction history
        cursor.execute("""
            SELECT
                Prediction_ID,
                Product_ID,
                Price,
                Discount,
                Previous_Sales,
                Predicted_Demand
            FROM Demand_Prediction
            ORDER BY Prediction_ID DESC
        """)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        # ==============================
        # CHECK HISTORY
        # ==============================

        if not rows:
            tk.Label(
                table_frame,
                text="No prediction history found.",
                font=("Segoe UI", 13),
                bg=WHITE,
                fg=SUBTEXT
            ).grid(
                row=1,
                column=0,
                columnspan=6,
                pady=50
            )
            return

        # ==============================
        # DISPLAY HISTORY
        # ==============================

        for row_number, row in enumerate(rows, start=1):
            for column, value in enumerate(row):
                if value is None:
                    value = "-"

                tk.Label(
                    table_frame,
                    text=str(value),
                    font=("Segoe UI", 10),
                    bg=WHITE,
                    fg=TEXT_COLOR,
                    padx=10,
                    pady=10
                ).grid(
                    row=row_number,
                    column=column,
                    sticky="nsew"
                )

        # ==============================
        # COLUMN WIDTH
        # ==============================

        for column in range(6):
            table_frame.columnconfigure(
                column,
                weight=1
            )

    except Exception as e:
        if conn:
            conn.close()

        messagebox.showerror(
            "History Error",
            str(e)
        )
