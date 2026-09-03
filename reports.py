import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection

# COLORS

BG_COLOR = "#f4f6f9"
WHITE = "#ffffff"
TEXT_COLOR = "#111827"
SUBTEXT = "#6b7280"
BLUE = "#2563eb"

# SHOW REPORTS

def show_reports(content):

    # Clear old page
    for widget in content.winfo_children():
        widget.destroy()
    # TITLE
    tk.Label(
        content,
        text="Demand Prediction Reports",
        font=("Segoe UI", 27, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=(25, 5))

    tk.Label(
        content,
        text="Product demand prediction results",
        font=("Segoe UI", 11),
        bg=BG_COLOR,
        fg=SUBTEXT
    ).pack(pady=(0, 20))

  
    # TABLE FRAME
    
    table_frame = tk.Frame(
        content,
        bg=WHITE,
        padx=20,
        pady=20,
        highlightbackground="#d1d5db",
        highlightthickness=1
    )

    table_frame.pack(
        padx=25,
        pady=10
    )

  
    # TABLE
  
    tree = ttk.Treeview(
        table_frame,
        columns=(
            "Prediction_ID",
            "Product_ID",
            "Predicted_Demand",
            "Prediction_Date"
        ),
        show="headings",
        height=12
    )

 
    # HEADINGS
   

    tree.heading(
        "Prediction_ID",
        text="Prediction ID"
    )

    tree.heading(
        "Product_ID",
        text="Product ID"
    )

    tree.heading(
        "Predicted_Demand",
        text="Predicted Demand"
    )

    tree.heading(
        "Prediction_Date",
        text="Prediction Date"
    )

   
    # COLUMN WIDTH
   
    tree.column(
        "Prediction_ID",
        width=130,
        anchor="center"
    )

    tree.column(
        "Product_ID",
        width=130,
        anchor="center"
    )

    tree.column(
        "Predicted_Demand",
        width=180,
        anchor="center"
    )

    tree.column(
        "Prediction_Date",
        width=160,
        anchor="center"
    )

    tree.pack()

    
    # LOAD REPORT DATA

    try:

        conn = get_connection()

        if conn is None:
            return

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                Prediction_ID,
                Product_ID,
                Predicted_Demand,
                Prediction_Date
            FROM Demand_Prediction
            ORDER BY Prediction_ID DESC
        """)

        rows = cursor.fetchall()

        for row in rows:
            tree.insert(
                "",
                "end",
                values=row
            )

        cursor.close()
        conn.close()

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    # TOTAL PREDICTED DEMAND

    try:

        conn = get_connection()

        if conn:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT COALESCE(
                    SUM(Predicted_Demand),
                    0
                )
                FROM Demand_Prediction
            """)

            total = cursor.fetchone()[0]

            cursor.close()
            conn.close()

            tk.Label(
                content,
                text=f"Total Predicted Demand: {float(total):.2f} Units",
                font=("Segoe UI", 16, "bold"),
                bg=BG_COLOR,
                fg=BLUE
            ).pack(
                pady=15
            )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )
