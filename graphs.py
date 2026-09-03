import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import get_connection

# COLORS
BG_COLOR = "#f4f6f9"
TEXT_COLOR = "#111827"
SUBTEXT = "#6b7280"

# SHOW GRAPH
def show_graph(content):
    # Clear old page
    for widget in content.winfo_children():
        widget.destroy()

    # TITLE
    tk.Label(
        content,
        text="Demand Prediction Graph",
        font=("Segoe UI", 27, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=(20, 5))

    tk.Label(
        content,
        text="Actual vs Predicted Quantity Sold",
        font=("Segoe UI", 11),
        bg=BG_COLOR,
        fg=SUBTEXT
    ).pack(pady=(0, 15))

    # GET SALES DATA
    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            Price,
            Discount,
            Previous_Sales,
            Quantity_Sold
        FROM Sales
        WHERE Price IS NOT NULL
        AND Discount IS NOT NULL
        AND Previous_Sales IS NOT NULL
        AND Quantity_Sold IS NOT NULL
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # CHECK DATA
    if len(rows) < 2:
        tk.Label(
            content,
            text="Not enough sales data for graph.",
            font=("Segoe UI", 15),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=50)
        return

    # DATAFRAME
    df = pd.DataFrame(
        rows,
        columns=[
            "Price",
            "Discount",
            "Previous_Sales",
            "Quantity_Sold"
        ]
    )

    # FEATURES
    X = df[
        [
            "Price",
            "Discount",
            "Previous_Sales"
        ]
    ]

    # TARGET
    y = df["Quantity_Sold"]

    # TRAIN MODEL
    model = LinearRegression()

    model.fit(
        X,
        y
    )

    # PREDICT
    predicted_values = model.predict(X)

    # GRAPH
    figure = plt.Figure(
        figsize=(8, 5),
        dpi=100
    )

    ax = figure.add_subplot(111)

    # Actual vs Predicted points
    ax.scatter(
        y,
        predicted_values,
        label="Actual vs Predicted"
    )

    # Prediction line
    ax.plot(
        [y.min(), y.max()],
        [y.min(), y.max()],
        label="Prediction Line"
    )

    ax.set_xlabel(
        "Actual Quantity Sold"
    )

    ax.set_ylabel(
        "Predicted Quantity Sold"
    )

    ax.set_title(
        "Product Demand Prediction Using Multiple Linear Regression"
    )

    ax.legend()
    ax.grid(True)

    # DISPLAY GRAPH
    canvas = FigureCanvasTkAgg(
        figure,
        master=content
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        pady=5
    )
