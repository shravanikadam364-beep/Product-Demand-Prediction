import tkinter as tk
from tkinter import ttk,messagebox
import pandas as pd
from sklearn.linear_model import LinearRegression
from database import get_connection

# ==============================
# COLORS
# ==============================
BG_COLOR="#f4f6f9"
WHITE="#ffffff"
TEXT_COLOR="#111827"
SUBTEXT="#6b7280"
BLUE="#2563eb"

# ==============================
# SHOW PREDICTION PAGE
# ==============================
def show_prediction(content):
    # Clear old page
    for widget in content.winfo_children():
        widget.destroy()

    # Page title
    tk.Label(
        content,
        text="Product Demand Prediction",
        font=("Segoe UI",27,"bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=(20,5))

    tk.Label(
        content,
        text="Multiple Linear Regression",
        font=("Segoe UI",11),
        bg=BG_COLOR,
        fg=SUBTEXT
    ).pack(pady=(0,15))

    # ==============================
    # FORM
    # ==============================
    form=tk.Frame(
        content,
        bg=WHITE,
        padx=35,
        pady=20,
        highlightbackground="#d1d5db",
        highlightthickness=1
    )
    form.pack()

    # Product ID
    tk.Label(
        form,
        text="Product ID",
        font=("Segoe UI",11),
        bg=WHITE
    ).grid(row=0,column=0,padx=10,pady=8,sticky="e")

    product_combo=ttk.Combobox(
        form,
        font=("Segoe UI",11),
        state="readonly",
        width=20
    )
    product_combo.grid(row=0,column=1,padx=10)

    # Price
    tk.Label(
        form,
        text="Price",
        font=("Segoe UI",11),
        bg=WHITE
    ).grid(row=1,column=0,padx=10,pady=8,sticky="e")

    price_entry=tk.Entry(
        form,
        font=("Segoe UI",11),
        width=22
    )
    price_entry.grid(row=1,column=1)

    # Discount
    tk.Label(
        form,
        text="Discount (%)",
        font=("Segoe UI",11),
        bg=WHITE
    ).grid(row=2,column=0,padx=10,pady=8,sticky="e")

    discount_entry=tk.Entry(
        form,
        font=("Segoe UI",11),
        width=22
    )
    discount_entry.grid(row=2,column=1)

    # Previous Sales
    tk.Label(
        form,
        text="Previous Sales",
        font=("Segoe UI",11),
        bg=WHITE
    ).grid(row=3,column=0,padx=10,pady=8,sticky="e")

    previous_entry=tk.Entry(
        form,
        font=("Segoe UI",11),
        width=22
    )
    previous_entry.grid(row=3,column=1)

    # ==============================
    # RESULT LABEL
    # ==============================
    result_label=tk.Label(
        content,
        text="Predicted Demand: -- Units",
        font=("Segoe UI",21,"bold"),
        bg=BG_COLOR,
        fg=BLUE
    )
    result_label.pack(pady=18)

    # ==============================
    # LOAD PRODUCT IDS
    # ==============================
    try:
        conn=get_connection()

        if conn:
            cursor=conn.cursor()

            cursor.execute("""
                SELECT Product_ID
                FROM Product
                ORDER BY Product_ID
            """)

            product_ids=[str(row[0]) for row in cursor.fetchall()]
            product_combo["values"]=product_ids

            cursor.close()
            conn.close()

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )

    # ==============================
    # LOAD PRODUCT PRICE
    # ==============================
    def load_product_price(event=None):
        try:
            product_id=int(product_combo.get())

            conn=get_connection()

            if conn is None:
                return

            cursor=conn.cursor()

            cursor.execute("""
                SELECT Price
                FROM Product
                WHERE Product_ID=%s
            """,(product_id,))

            result=cursor.fetchone()

            if result:
                price_entry.delete(0,tk.END)
                price_entry.insert(0,str(result[0]))

            cursor.close()
            conn.close()

        except Exception:
            pass

    product_combo.bind(
        "<<ComboboxSelected>>",
        load_product_price
    )

    # ==============================
    # PREDICT DEMAND
    # ==============================
    def predict_demand():
        try:
            # Check Product ID
            if product_combo.get()=="":
                messagebox.showwarning(
                    "Warning",
                    "Please select Product ID."
                )
                return

            product_id=int(product_combo.get())

            # Get input values
            price=float(price_entry.get())
            discount=float(discount_entry.get())
            previous_sales=float(previous_entry.get())

            # ==============================
            # GET TRAINING DATA
            # ==============================
            conn=get_connection()

            if conn is None:
                return

            cursor=conn.cursor()

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

            rows=cursor.fetchall()

            cursor.close()
            conn.close()

            # Check training data
            if len(rows)<2:
                messagebox.showerror(
                    "Error",
                    "Not enough sales data for ML prediction."
                )
                return

            # ==============================
            # CREATE DATAFRAME
            # ==============================
            df=pd.DataFrame(
                rows,
                columns=[
                    "Price",
                    "Discount",
                    "Previous_Sales",
                    "Quantity_Sold"
                ]
            )

            # Features
            X=df[
                [
                    "Price",
                    "Discount",
                    "Previous_Sales"
                ]
            ]

            # Target
            y=df["Quantity_Sold"]

            # ==============================
            # MULTIPLE LINEAR REGRESSION
            # ==============================
            model=LinearRegression()
            model.fit(X,y)

            # New input data
            new_data=pd.DataFrame({
                "Price":[price],
                "Discount":[discount],
                "Previous_Sales":[previous_sales]
            })

            # Prediction
            prediction=model.predict(new_data)

            predicted_demand=round(
                float(prediction[0]),
                2
            )

            # Demand cannot be negative
            if predicted_demand<0:
                predicted_demand=0

            # Display result
            result_label.config(
                text=f"Predicted Demand: {predicted_demand} Units"
            )

            # ==============================
            # SAVE PREDICTION
            # ==============================
            conn=get_connection()

            if conn is None:
                return

            cursor=conn.cursor()

            # Prediction_ID is auto_increment
            # Save all prediction input values
            cursor.execute("""
                INSERT INTO Demand_Prediction
                (
                    Product_ID,
                    Price,
                    Discount,
                    Previous_Sales,
                    Predicted_Demand
                )
                VALUES
                (%s,%s,%s,%s,%s)
            """,(
                product_id,
                price,
                discount,
                previous_sales,
                predicted_demand
            ))

            conn.commit()

            cursor.close()
            conn.close()

            # Success message
            messagebox.showinfo(
                "Prediction Result",
                f"Predicted Demand:\n\n{predicted_demand} Units"
            )

        except ValueError:
            messagebox.showerror(
                "Invalid Data",
                "Please enter valid numeric values."
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # ==============================
    # PREDICT BUTTON
    # ==============================
    tk.Button(
        form,
        text="PREDICT DEMAND",
        command=predict_demand,
        font=("Segoe UI",12,"bold"),
        bg=BLUE,
        fg=WHITE,
        activebackground="#1d4ed8",
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        width=20,
        pady=9
    ).grid(row=4,column=1,pady=15)
