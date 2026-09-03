import mysql.connector
from tkinter import messagebox

# DATABASE SETTINGS

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root123"
DB_NAME = "ProductDemandDB"

# DATABASE CONNECTION

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn

    except mysql.connector.Error as e:
        messagebox.showerror(
            "Database Error",
            f"Unable to connect to database.\n\n{e}"
        )
        return None

# GET PRODUCT COUNT

def get_product_count():
    conn = get_connection()

    if conn is None:
        return 0

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM Product"
    )

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return count

# GET SALES COUNT

def get_sales_count():
    conn = get_connection()

    if conn is None:
        return 0

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM Sales"
    )

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return count

# GET PREDICTION COUNT

def get_prediction_count():
    conn = get_connection()

    if conn is None:
        return 0

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM Demand_Prediction"
    )

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return count

# GET TOTAL PREDICTED DEMAND

def get_total_predicted_demand():
    conn = get_connection()

    if conn is None:
        return 0

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

    return float(total)

# TEST CONNECTION

if __name__ == "__main__":
    connection = get_connection()

    if connection:
        print("Database connected successfully!")
        connection.close()
