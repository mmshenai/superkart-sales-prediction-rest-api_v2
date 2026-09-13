import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860" # Assuming 'backend' is the service name in Docker Compose

# Set the title of the Streamlit app
st.title("SuperKart Sales Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for product and store features
product_weight = st.number_input("Product Weight", min_value=4.0, max_value=22.0, value=12.0)
product_sugar_content = st.selectbox("Product Sugar Content", ['Low Sugar', 'Regular', 'No Sugar'])
product_allocated_area = st.number_input("Product Allocated Area", min_value=0.004, max_value=0.298, value=0.07, format="%.3f")
product_type = st.selectbox("Product Type", ['Frozen Foods', 'Dairy', 'Canned', 'Baking Goods', 'Health and Hygiene', 'Breakfast', 'Soft Drinks', 'Fruits and Vegetables', 'Household', 'Snack Foods', 'Meat', 'Hard Drinks', 'Breads', 'Starchy Foods', 'Others', 'Seafood'])
product_mrp = st.number_input("Product MRP", min_value=31.0, max_value=266.0, value=150.0)
store_establishment_year = st.number_input("Store Establishment Year", min_value=1987, max_value=2009, value=1999, step=1)
store_size = st.selectbox("Store Size", ['Medium', 'High', 'Small'])
store_location_city_type = st.selectbox("Store Location City Type", ['Tier 2', 'Tier 1', 'Tier 3'])
store_type = st.selectbox("Store Type", ['Supermarket Type2', 'Departmental Store', 'Supermarket Type1', 'Food Mart'])

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_Weight': product_weight,
    'Product_Sugar_Content': product_sugar_content,
    'Product_Allocated_Area': product_allocated_area,
    'Product_Type': product_type,
    'Product_MRP': product_mrp,
    'Store_Establishment_Year': store_establishment_year,
    'Store_Size': store_size,
    'Store_Location_City_Type': store_location_city_type,
    'Store_Type': store_type
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/sales", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted Product Store Sales Total']
        st.success(f"Predicted Product Store Sales Total: {prediction:.2f}")
    else:
        st.error(f"Error connecting to the prediction API. Status code: {response.status_code}. Response: {response.text}")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        # The Flask API expects the file to be sent directly, not as a dictionary in json
        response = requests.post(f"{BACKEND_URL}/v1/salesbatch", files={"file": uploaded_file.getvalue()})
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(pd.DataFrame(predictions))
        else:
            st.error(f"Error connecting to the prediction API. Status code: {response.status_code}. Response: {response.text}")
