# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_sales_predictor_api = Flask("SuperKart Sales Predictor")

# Load the trained machine learning model
model = joblib.load('random_forest_regressor_model.joblib')

# Define a route for the home page (GET request)
@superkart_sales_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Sales Prediction API!"

# Define an endpoint for single property prediction (POST request)
@superkart_sales_predictor_api.post('/v1/sales')
def predict_sales():
    """
    This function handles POST requests to the '/v1/sales' endpoint.
    It expects a JSON payload containing product and store details and returns
    the predicted sales as a JSON response.
    """
    # Get the JSON data from the request body
    item_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': item_data['Product_Weight'],
        'Product_Sugar_Content': item_data['Product_Sugar_Content'],
        'Product_Allocated_Area': item_data['Product_Allocated_Area'],
        'Product_Type': item_data['Product_Type'],
        'Product_MRP': item_data['Product_MRP'],
        'Store_Establishment_Year': item_data['Store_Establishment_Year'],
        'Store_Size': item_data['Store_Size'],
        'Store_Location_City_Type': item_data['Store_Location_City_Type'],
        'Store_Type': item_data['Store_Type']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction
    predicted_sales = model.predict(input_data)[0]

    # Convert predicted_sales to Python float and round
    predicted_sales = round(float(predicted_sales), 2)

    # Return the predicted sales
    return jsonify({'Predicted Product Store Sales Total': predicted_sales})


# Define an endpoint for batch prediction (POST request)
@superkart_sales_predictor_api.post('/v1/salesbatch')
def predict_sales_batch():
    """
    This function handles POST requests to the '/v1/salesbatch' endpoint.
    It expects a CSV file containing product and store details for multiple items
    and returns the predicted sales as a list in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all items in the DataFrame
    predicted_sales_list = model.predict(input_data).tolist()

    # Round predictions
    predicted_sales_list = [round(float(sales), 2) for sales in predicted_sales_list]

    # Return the predictions list as a JSON response
    return jsonify({'Predicted Sales': predicted_sales_list})

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    superkart_sales_predictor_api.run(debug=True)
