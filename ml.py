import pandas as pd
from sklearn.linear_model import LinearRegression

# Sales Data
data = {
    "Price": [100, 120, 150, 130, 110, 160, 140, 125, 180, 170],
    "Discount": [5, 10, 8, 12, 5, 15, 10, 7, 20, 15],
    "Previous_Sales": [50, 55, 60, 58, 52, 65, 62, 57, 70, 68],
    "Quantity_Sold": [45, 50, 55, 53, 48, 60, 57, 52, 65, 63]
}

# Create DataFrame
df = pd.DataFrame(data)

# Input Variables
X = df[["Price", "Discount", "Previous_Sales"]]

# Target Variable
y = df["Quantity_Sold"]

# Multiple Linear Regression
model = LinearRegression()

# Train Model
model.fit(X, y)

# New Product Data
new_data = pd.DataFrame({
    "Price": [100],
    "Discount": [5],
    "Previous_Sales": [50]
})

# Predict Demand
prediction = model.predict(new_data)

print("Predicted Product Demand:", round(prediction[0], 2))
