import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection

BG_COLOR = "#f4f6f9"
WHITE = "#ffffff"
TEXT_COLOR = "#111827"
SUBTEXT = "#6b7280"
BLUE = "#2563eb"


def show_products(content):

    # Clear old page
    for widget in content.winfo_children():
        widget.destroy()

    # Title
    tk.Label(
        content,
        text="Product Management",
        font=("Segoe UI", 27, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=(20, 5))

    tk.Label(
        content,
        text="Add and manage product details",
        font=("Segoe UI", 11),
        bg=BG_COLOR,
        fg=SUBTEXT
    ).pack(pady=(0, 12))

    # Form
    form = tk.Frame(
        content,
        bg=WHITE,
        padx=25,
        pady=12,
        highlightbackground="#d1d5db",
        highlightthickness=1
    )

    form.pack()

    # Product ID
    tk.Label(
        form,
        text="Product ID",
        font=("Segoe UI", 11),
        bg=WHITE
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=5,
        sticky="e"
    )

    product_id_entry = tk.Entry(
        form,
        font=("Segoe UI", 11),
        width=22
    )

    product_id_entry.grid(
        row=0,
        column=1,
        padx=10
    )

    # Product Name
    tk.Label(
        form,
        text="Product Name",
        font=("Segoe UI", 11),
        bg=WHITE
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=5,
        sticky="e"
    )

    product_name_entry = tk.Entry(
        form,
        font=("Segoe UI", 11),
        width=22
    )

    product_name_entry.grid(
        row=1,
        column=1,
        padx=10
    )

    # Category
    tk.Label(
        form,
        text="Category",
        font=("Segoe UI", 11),
        bg=WHITE
    ).grid(
        row=2,
        column=0,
        padx=10,
        pady=5,
        sticky="e"
    )

    category_entry = tk.Entry(
        form,
        font=("Segoe UI", 11),
        width=22
    )

    category_entry.grid(
        row=2,
        column=1,
        padx=10
    )

    # Price
    tk.Label(
        form,
        text="Price",
        font=("Segoe UI", 11),
        bg=WHITE
    ).grid(
        row=3,
        column=0,
        padx=10,
        pady=5,
        sticky="e"
    )

    price_entry = tk.Entry(
        form,
        font=("Segoe UI", 11),
        width=22
    )

    price_entry.grid(
        row=3,
        column=1,
        padx=10
    )

    # Add Product Function
    def add_product():

        try:
            product_id = int(product_id_entry.get())
            product_name = product_name_entry.get().strip()
            category = category_entry.get().strip()
            price = float(price_entry.get())

            # Check empty values
            if not product_name or not category:
                messagebox.showwarning(
                    "Warning",
                    "Please enter all product details."
                )
                return

            # Database connection
            conn = get_connection()

            if conn is None:
                return

            cursor = conn.cursor()

            # Insert product
            cursor.execute("""
                INSERT INTO Product
                (
                    Product_ID,
                    Product_Name,
                    Category,
                    Price
                )
                VALUES (%s, %s, %s, %s)
            """, (
                product_id,
                product_name,
                category,
                price
            ))

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Product added successfully!"
            )

            # Refresh page
            show_products(content)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Product ID and Price must be valid numbers."
            )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # Add Button
    tk.Button(
        form,
        text="Add Product",
        command=add_product,
        font=("Segoe UI", 10, "bold"),
        bg=BLUE,
        fg=WHITE,
        activebackground="#1d4ed8",
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=6
    ).grid(
        row=4,
        column=1,
        pady=8
    )

    # Product Table
    table_frame = tk.Frame(
        content,
        bg=BG_COLOR
    )

    table_frame.pack(
        pady=20
    )

    tree = ttk.Treeview(
        table_frame,
        columns=(
            "ID",
            "Name",
            "Category",
            "Price"
        ),
        show="headings",
        height=10
    )

    # Table Headings
    tree.heading(
        "ID",
        text="Product ID"
    )

    tree.heading(
        "Name",
        text="Product Name"
    )

    tree.heading(
        "Category",
        text="Category"
    )

    tree.heading(
        "Price",
        text="Price"
    )

    # Column Width
    tree.column(
        "ID",
        width=100,
        anchor="center"
    )

    tree.column(
        "Name",
        width=200,
        anchor="center"
    )

    tree.column(
        "Category",
        width=180,
        anchor="center"
    )

    tree.column(
        "Price",
        width=120,
        anchor="center"
    )

    tree.pack()

    # Load Products
    try:
        conn = get_connection()

        if conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    Product_ID,
                    Product_Name,
                    Category,
                    Price
                FROM Product
                ORDER BY Product_ID
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
            "Error",
            str(e)
        )
