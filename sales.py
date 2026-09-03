import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from database import get_connection

# COLORS
BG_COLOR = "#f4f6f9"
WHITE = "#ffffff"
TEXT_COLOR = "#111827"
SUBTEXT = "#6b7280"
BLUE = "#2563eb"
GREEN = "#16a34a"

# SHOW SALES PAGE

def show_sales(content):

    # Clear old page
    for widget in content.winfo_children():
        widget.destroy()

    # TITLE

    tk.Label(
        content,
        text="Sales Management",
        font=("Segoe UI", 27, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=(15, 3))


    tk.Label(
        content,
        text="Add and manage sales records",
        font=("Segoe UI", 11),
        bg=BG_COLOR,
        fg=SUBTEXT
    ).pack(pady=(0, 8))

    # FORM
    form = tk.Frame(
        content,
        bg=WHITE,
        padx=25,
        pady=8,
        highlightbackground="#d1d5db",
        highlightthickness=1
    )

    form.pack()

    # PRODUCT ID
    tk.Label(
        form,
        text="Product ID",
        font=("Segoe UI", 10),
        bg=WHITE
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=3,
        sticky="e"
    )

    product_combo = ttk.Combobox(
        form,
        font=("Segoe UI", 10),
        state="readonly",
        width=20
    )

    product_combo.grid(
        row=0,
        column=1,
        padx=10
    )

    # SALE DATE

    tk.Label(
        form,
        text="Sale Date",
        font=("Segoe UI", 10),
        bg=WHITE
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=3,
        sticky="e"
    )


    date_entry = tk.Entry(
        form,
        font=("Segoe UI", 10),
        width=22
    )

    date_entry.insert(
        0,
        str(date.today())
    )

    date_entry.grid(
        row=1,
        column=1,
        padx=10
    )
    # MONTH
    tk.Label(
        form,
        text="Month",
        font=("Segoe UI", 10),
        bg=WHITE
    ).grid(
        row=2,
        column=0,
        padx=10,
        pady=3,
        sticky="e"
    )


    month_entry = tk.Entry(
        form,
        font=("Segoe UI", 10),
        width=22
    )

    month_entry.grid(
        row=2,
        column=1,
        padx=10
    )

    # QUANTITY SOLD
    tk.Label(
        form,
        text="Quantity Sold",
        font=("Segoe UI", 10),
        bg=WHITE
    ).grid(
        row=3,
        column=0,
        padx=10,
        pady=3,
        sticky="e"
    )


    quantity_entry = tk.Entry(
        form,
        font=("Segoe UI", 10),
        width=22
    )

    quantity_entry.grid(
        row=3,
        column=1,
        padx=10
    )

    # PRICE

    tk.Label(
        form,
        text="Price",
        font=("Segoe UI", 10),
        bg=WHITE
    ).grid(
        row=4,
        column=0,
        padx=10,
        pady=3,
        sticky="e"
    )


    price_entry = tk.Entry(
        form,
        font=("Segoe UI", 10),
        width=22
    )

    price_entry.grid(
        row=4,
        column=1,
        padx=10
    )

    # DISCOUNT
    tk.Label(
        form,
        text="Discount (%)",
        font=("Segoe UI", 10),
        bg=WHITE
    ).grid(
        row=5,
        column=0,
        padx=10,
        pady=3,
        sticky="e"
    )
    discount_entry = tk.Entry(
        form,
        font=("Segoe UI", 10),
        width=22
    )
    discount_entry.grid(
        row=5,
        column=1,
        padx=10
    )

    # PREVIOUS SALES

    tk.Label(
        form,
        text="Previous Sales",
        font=("Segoe UI", 10),
        bg=WHITE
    ).grid(
        row=6,
        column=0,
        padx=10,
        pady=3,
        sticky="e"
    )


    previous_entry = tk.Entry(
        form,
        font=("Segoe UI", 10),
        width=22
    )

    previous_entry.grid(
        row=6,
        column=1,
        padx=10
    )

    # LOAD PRODUCT IDs

    try:

        conn = get_connection()

        if conn:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT Product_ID
                FROM Product
                ORDER BY Product_ID
            """)

            product_ids = [
                str(row[0])
                for row in cursor.fetchall()
            ]

            product_combo["values"] = product_ids

            cursor.close()
            conn.close()

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    # LOAD PRODUCT PRICE

    def load_product_price(event=None):

        try:

            product_id = int(
                product_combo.get()
            )


            conn = get_connection()

            if conn is None:
                return


            cursor = conn.cursor()


            cursor.execute("""
                SELECT Price
                FROM Product
                WHERE Product_ID = %s
            """, (product_id,))


            result = cursor.fetchone()


            if result:

                price_entry.delete(
                    0,
                    tk.END
                )

                price_entry.insert(
                    0,
                    str(result[0])
                )


            cursor.close()
            conn.close()


        except Exception:

            pass


    product_combo.bind(
        "<<ComboboxSelected>>",
        load_product_price
    )
    # ADD SALES
   
    def add_sale():

        try:

            # Product ID

            if product_combo.get() == "":

                messagebox.showwarning(
                    "Warning",
                    "Please select Product ID." )

                return
            product_id = int(
                product_combo.get()
            )
            # Date

            sale_date = (
                date_entry.get().strip()
            )
            # Month

            month = int(
                month_entry.get()
            )

            if month < 1 or month > 12:

                messagebox.showwarning(
                    "Warning",
                    "Month must be between 1 and 12.")
                return


            # Quantity
            quantity = int(
                quantity_entry.get()
            )

            # Price
            price = float(
                price_entry.get()
            )

            # Discount
            discount = float(
                discount_entry.get()
            )
            # Previous Sales

            previous_sales = float(
                previous_entry.get()
            )
            # DATABASE

            conn = get_connection()

            if conn is None:
                return
            cursor = conn.cursor()

            # GENERATE SALES ID
            cursor.execute("""
                SELECT COALESCE(
                    MAX(Sales_ID),
                    0
                ) + 1
                FROM Sales
            """)


            next_sales_id = cursor.fetchone()[0]

            # INSERT SALES
            cursor.execute("""
                INSERT INTO Sales
                (
                    Sales_ID,
                    Product_ID,
                    Sale_Date,
                    Month,
                    Quantity_Sold,
                    Price,
                    Discount,
                    Previous_Sales
                )
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
              """, (
              next_sales_id,
              product_id,
              sale_date,
              month,
              quantity,
              price,
              discount,
              previous_sales
                ))

            conn.commit()


            cursor.close()
            conn.close()


            messagebox.showinfo(
                "Success",
                "Sales record added successfully!"
            )


            # Refresh page

            show_sales(content)


        except ValueError:

            messagebox.showerror(
                "Invalid Data",
                "Please enter valid numeric values."
            )


        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # ADD SALES BUTTON

    tk.Button(
        form,
        text="Add Sales",
        command=add_sale,
        font=("Segoe UI", 10, "bold"),
        bg=GREEN,
        fg=WHITE,
        activebackground="#15803d",
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=5
    ).grid(
        row=7,
        column=1,
        pady=7
    )

    # SALES TABLE

    table_frame = tk.Frame(
        content,
        bg=BG_COLOR
    )

    table_frame.pack(
        pady=8
    )


    tree = ttk.Treeview(
        table_frame,
        columns=(
            "Sales_ID",
            "Product_ID",
            "Sale_Date",
            "Month",
            "Quantity",
            "Price",
            "Discount",
            "Previous"
        ),
        show="headings",
        height=7
    )

    # TABLE HEADINGS

    tree.heading(
        "Sales_ID",
        text="Sales ID"
    )

    tree.heading(
        "Product_ID",
        text="Product ID"
    )

    tree.heading(
        "Sale_Date",
        text="Sale Date"
    )

    tree.heading(
        "Month",
        text="Month"
    )

    tree.heading(
        "Quantity",
        text="Quantity Sold"
    )

    tree.heading(
        "Price",
        text="Price"
    )

    tree.heading(
        "Discount",
        text="Discount"
    )

    tree.heading(
        "Previous",
        text="Previous Sales"
    )
    # TABLE WIDTH

    tree.column(
        "Sales_ID",
        width=65,
        anchor="center"
    )

    tree.column(
        "Product_ID",
        width=70,
        anchor="center"
    )

    tree.column(
        "Sale_Date",
        width=90,
        anchor="center"
    )

    tree.column(
        "Month",
        width=55,
        anchor="center"
    )

    tree.column(
        "Quantity",
        width=90,
        anchor="center"
    )

    tree.column(
        "Price",
        width=80,
        anchor="center"
    )

    tree.column(
        "Discount",
        width=70,
        anchor="center"
    )

    tree.column(
        "Previous",
        width=100,
        anchor="center"
    )

    tree.pack()
    # LOAD SALES DATA
  
    try:

        conn = get_connection()

        if conn:

            cursor = conn.cursor()


            cursor.execute("""
                SELECT
                    Sales_ID,
                    Product_ID,
                    Sale_Date,
                    Month,
                    Quantity_Sold,
                    Price,
                    Discount,
                    Previous_Sales
                FROM Sales
                ORDER BY Sales_ID
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
