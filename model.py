import pandas as pd
import pickle
import csv

def encode_5():

    # Define custom encoding functions
    def encode_cars(value):
        return int((value + 1) / 2)  # Encode as every two consecutive integers

    def encode_month(value):
        return int((value + 1) / 2)  # Encode as every two consecutive integers starting from 1

    def encode_hour(value):
        return int(value / 2)  # Encode as integer division

    def encode_rain(value):
        return int(value / 10)  # Encode as integer division

    def encode_fog(value):
        return int(value / 10)  # Encode as integer division

    # Load data from CSV file
    df = pd.read_csv('test.csv')

    # Apply custom encoding functions to each column
    df['cars'] = df['cars'].apply(encode_cars)
    df['month'] = df['month'].apply(encode_month)
    df['hour'] = df['hour'].apply(encode_hour)
    df['rain'] = df['rain'].apply(encode_rain)
    df['fog'] = df['fog'].apply(encode_fog)

    # Save the encoded DataFrame to a new CSV file
    df.to_csv('encoded_test.csv', index=False)

def predict():
    # Load the pre-trained model from the .pkl file
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)

    # Read the CSV file containing the features
    data = pd.read_csv('encoded_test.csv')

    # Extract the features from the data
    features = data[['cars', 'month', 'hour', 'rain', 'fog']].values

    # Predict using the loaded model
    predictions = model.predict(features)

    # Create a DataFrame for the predictions
    result_df = pd.DataFrame({'light': predictions})

    # Save the predictions to a CSV file
    result_df.to_csv('result.csv', index=False)

def decode_1():
    # Define custom decoding functions
    def decode_light(value):
        return value * 6 + 1

    # Load data from CSV file
    df_encoded = pd.read_csv('result.csv')

    # Apply custom decoding functions to each column
    df_encoded['light'] = df_encoded['light'].apply(decode_light)

    # Save the decoded DataFrame to a new CSV file
    df_encoded.to_csv('decoded_result.csv', index=False)

def run():
    encode_5()
    predict()
    decode_1()
    with open('decoded_result.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            return row[0]

def save_to_csv(data_list, filename):
    headers = ['cars', 'month', 'hour', 'rain', 'fog']
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerow({
            'cars': data_list[0],
            'month': data_list[1],
            'hour': data_list[2],
            'rain': data_list[3],
            'fog': data_list[4]
        })

def get_light(file_name):
    # Open the CSV file
    with open(file_name, 'r') as file:
        # Create a CSV reader object
        reader = csv.reader(file)        
        # Skip the header row
        next(reader)       
        # Get the second row
        second_row = next(reader)      
        # Get the first element of the second row
        first_number = second_row[0]       
        # Return the first number
        return first_number