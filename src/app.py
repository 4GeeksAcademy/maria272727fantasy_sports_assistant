import streamlit as st
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset from the pickle file
data_path = '/workspaces/maria272727fantasy_sports_assistant/data/parsed_data_all_positions.pkl'

# Load the data (assuming it's a pickle file containing a DataFrame)
with open(data_path, 'rb') as f:
    data_df = pickle.load(f)

# Ensure that the 'Name' column exists in your dataset
if 'Name' not in data_df.columns:
    st.error("Error: 'Name' column not found in dataset!")
else:
    # Title and description of the app with color
    st.markdown("""
        <style>
            .title {
                color: #1f77b4;
                font-size: 36px;
                font-weight: bold;
            }
            .header {
                background-color: #f0f2f6;
                padding: 10px;
                font-size: 24px;
                color: #333;
            }
            .footer {
                background-color: #f0f2f6;
                text-align: center;
                padding: 10px;
                font-size: 14px;
                color: #888;
            }
            .sidebar .sidebar-content {
                background-color: #e0e5e8;
            }
        </style>
        <div class="title">Fantasy Football Points Prediction</div>
    """, unsafe_allow_html=True)

    # User-friendly description
    st.markdown("""
        ### Welcome to the Fantasy Football Points Prediction App
        This app predicts fantasy football points based on the player's details. For now, the prediction is random. 
        You can enter the player's name, and we'll predict their fantasy points.
    """)

    # Sidebar: Select player from dataset
    st.sidebar.title("Player Details")
    player_name = st.sidebar.selectbox("Select a Player", data_df['Name'].unique())

    # Get selected player's data
    player_data = data_df[data_df['Name'] == player_name].iloc[0]

    # Show player's stats in sidebar
    st.sidebar.subheader(f"{player_name}'s Stats")
    st.sidebar.write(f"Age: {player_data['Age']}")
    st.sidebar.write(f"Experience: {player_data['Exp']} years")
    st.sidebar.write(f"Games Played: {player_data['G']}")
    st.sidebar.write(f"Completions: {player_data['Cmp']}")

    # Display player info on main page
    st.write(f"### {player_name}'s Fantasy Stats")
    st.write(f"Age: {player_data['Age']}, Experience: {player_data['Exp']} years")
    st.write(f"Games Played: {player_data['G']}, Completions: {player_data['Cmp']}")

    # Create a plot for the selected player
    fig, ax = plt.subplots(figsize=(6, 4))
    stats = ['Games Played', 'Completions']
    values = [player_data['G'], player_data['Cmp']]
    ax.bar(stats, values, color=['#1f77b4', '#ff7f0e'])

    ax.set_title(f"Stats of {player_name}")
    ax.set_ylabel('Value')
    ax.set_xlabel('Stats')

    # Show the plot
    st.pyplot(fig)

    # Prediction Section (Dummy model: Random prediction)
    if st.button('Predict Fantasy Points'):
        # Dummy prediction: Random value between 50 and 300
        prediction = np.random.randint(50, 300)
        st.success(f'Predicted Fantasy Points for {player_name}: **{prediction}**')

    # Footer (Optional)
    st.markdown("""
        <div class="footer">
            Powered by Streamlit | Fantasy Sports Assistant
        </div>
    """, unsafe_allow_html=True)