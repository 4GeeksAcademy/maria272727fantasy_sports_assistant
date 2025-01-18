import streamlit as st
import joblib
import numpy as np

# Load the pre-trained model
model = joblib.load('best_rf_model.pkl')

# Streamlit user interface (UI)
st.title('Fantasy Football Points Prediction')

# Create input fields for the 189 features (the ones used to train the model)

# You may need to replace the following inputs with the actual features used to train the model.
age = st.number_input('Age', min_value=18, max_value=40)
exp = st.number_input('Experience (Years)', min_value=1, max_value=20)
g = st.number_input('Games Played', min_value=0, max_value=16)
cmp = st.number_input('Completions', min_value=0, max_value=50)
att = st.number_input('Attempts', min_value=0, max_value=50)

# Add more inputs as needed to match the training features
# For example:
# stat1 = st.number_input('Feature 1')
# stat2 = st.number_input('Feature 2')
# stat3 = st.number_input('Feature 3')

# Example array to hold all 189 features
input_features = np.array([age, exp, g, cmp, att])  # Add other features here as placeholders

# Make prediction when the "Predict" button is clicked
if st.button('Predict'):
    # Make prediction using the trained model
    try:
        prediction = model.predict(input_features.reshape(1, -1))  # Reshaping to 2D array as model expects
        st.write(f'Predicted Fantasy Points: {prediction[0]}')
    except Exception as e:
        st.write(f'Error during prediction: {e}')