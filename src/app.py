import streamlit as st
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# Direct image URL from Imgur
background_url = "https://i.imgur.com/WcakZvJ.jpg"

# Apply the background image via custom CSS
st.markdown(f"""
    <style>
        body {{
            background-image: url('{background_url}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .stApp {{
            background-color: rgba(0, 0, 0, 0.5);  /* Semi-transparent black overlay */
        }}
        .title {{
            color: #FFFFFF;
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
        }}
        .header {{
            background-color: rgba(240, 242, 246, 0.7); /* Light grey with transparency */
            padding: 10px;
            font-size: 24px;
            color: #FFFFFF;  /* White text */
            text-align: center;
        }}
        .footer {{
            background-color: rgba(240, 242, 246, 0.7);
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: #FFFFFF;  /* White text */
            margin-top: 30px;
        }}
        .intro {{
            color: #FFFFFF;  /* White text for the intro */
            font-size: 18px;
            text-align: center;
        }}
        .sidebar .player_stats {{
            color: #000000;  /* Black text for the player's stats in the sidebar */
            font-size: 16px;
            text-align: left;
            margin-top: 20px;
        }}
        .main_page .player_stats {{
            color: #FFFFFF;  /* White text for the player's stats on the main page */
            font-size: 16px;
            text-align: left;
            margin-top: 20px;
        }}
        .projected_points {{
            color: #000000;  /* Black text for the projected fantasy points message */
            font-size: 18px;
            font-weight: bold;
            text-align: center;
        }}
        .prediction_result {{
            color: #000000;  /* Black text for the prediction result */
            font-size: 18px;
            font-weight: bold;
            text-align: center;
        }}
    </style>
""", unsafe_allow_html=True)

# Display the logo in the top left corner
logo_path = './src/score_castlogo.png'
st.image(logo_path, width=100)  # Adjust width as needed

# Load your dataset from the pickle file
data_path = './data/parsed_data_all_positions.pkl'

# Load the data (assuming it's a pickle file containing a DataFrame)
with open(data_path, 'rb') as f:
    data_df = pickle.load(f)

# Ensure that the 'Name' column exists in your dataset
if 'Name' not in data_df.columns:
    st.error("Error: 'Name' column not found in dataset!")
else:
    # Title and description of the app with color
    st.markdown("""
        <div class="title">ScoreCast: Fantasy Football Points Prediction</div>
    """, unsafe_allow_html=True)

    # User-friendly description with white text
    st.markdown("""
        <div class="intro">
            ### Welcome to **ScoreCast**, your ultimate Fantasy Football Points Prediction tool.
            <br><br>
            **ScoreCast** leverages the power of data to help you predict fantasy football points for players based on their performance stats. Whether you are managing your fantasy team or just looking to forecast player potential, **ScoreCast** provides quick and reliable projections for the upcoming weeks.
            <br><br>
            Enter a player's name from the list, and we'll predict their fantasy points for the next set of games.
        </div>
    """, unsafe_allow_html=True)

    # Sidebar: Select player from dataset
    st.sidebar.title("Player Details")
    player_name = st.sidebar.selectbox("Select a Player", data_df['Name'].unique())

    # Get selected player's data
    player_data = data_df[data_df['Name'] == player_name].iloc[0]

    # Show player's stats in sidebar (with black color for stats)
    st.sidebar.subheader(f"{player_name}'s Stats")
    st.sidebar.markdown(f"<div class='sidebar player_stats'>Age: {player_data['Age']}</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div class='sidebar player_stats'>Experience: {player_data['Exp']} years</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div class='sidebar player_stats'>Games Played: {player_data['G']}</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div class='sidebar player_stats'>Completions: {player_data['Cmp']}</div>", unsafe_allow_html=True)

    # Display player info on main page (with white color for stats)
    st.write(f"### {player_name}'s Fantasy Stats")
    st.markdown(f"<div class='main_page player_stats'>Age: {player_data['Age']}, Experience: {player_data['Exp']} years</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='main_page player_stats'>Games Played: {player_data['G']}, Completions: {player_data['Cmp']}</div>", unsafe_allow_html=True)

    # Get the past few weeks of fantasy points for this player
    # Assuming you have a column 'FantPt' for Fantasy Points and 'Week' for week number or date
    recent_weeks = data_df[data_df['Name'] == player_name].sort_values('Week', ascending=False).head(5)
    fantasy_points = recent_weeks['FantPt'].values  # Get the fantasy points of the last few games
    weeks = recent_weeks['Week'].values  # Get the corresponding week numbers (or dates)

    # Create a line plot showing the fantasy points over the past few weeks
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(weeks, fantasy_points, marker='o', color='b', label='Fantasy Points')

    # Make a prediction for the next week (using the same random prediction for now)
    next_week = weeks[0] + 1  # Assuming the next week is just the next sequential week
    predicted_points = np.random.randint(0, 51)  # Dummy prediction
    ax.plot(next_week, predicted_points, marker='x', color='r', label='Predicted Fantasy Points')

    # Add labels and title
    ax.set_xlabel('Weeks')
    ax.set_ylabel('Fantasy Points')
    ax.set_title(f'{player_name} - Fantasy Points Over the Last Few Weeks & Prediction for Next Game')
    ax.legend()

    # Display the plot
    st.pyplot(fig)

    # Prediction Section (Projected fantasy points for the upcoming weeks)
    st.markdown(f"<div class='projected_points'>Projected Fantasy Points for {player_name} in the upcoming weeks: {predicted_points}</div>", unsafe_allow_html=True)

    # Prediction Result Section (this will be black now)
    st.markdown(f"<div class='prediction_result'>Fantasy Points Prediction for {player_name}: {predicted_points}</div>", unsafe_allow_html=True)

    # Footer (Optional)
    st.markdown("""
        <div class="footer">
            Powered by Streamlit | Fantasy Sports Assistant
        </div>
    """, unsafe_allow_html=True)