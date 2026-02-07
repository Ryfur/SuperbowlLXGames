import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Set up the page
st.set_page_config(page_title="Super Bowl LX Leaderboard", layout="centered")
st.title("🏆 Super Bowl LX Prop Leaderboard")

# 1. Connect to Google Sheets
# You will set the URL in the Streamlit Cloud dashboard later
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Read the two tabs (Dataframes)
# Replace 'Form Responses 1' and 'Master Key' with your actual tab names
df_responses = conn.read(worksheet="Form Responses 1")
df_key = conn.read(worksheet="Master Key")

# 3. Scoring Logic
def calculate_player_score(row, key):
    score = 0
    # Logic: compare each prop column starting after the 'Name' column
    # Adjust the slice [3:] if your Name column is at a different index
    for col in df_responses.columns[3:]:
        user_val = str(row[col]).strip().lower()
        correct_val = str(key[col].values[0]).strip().lower()
        
        # Only score if the Master Key has an actual answer filled in
        if correct_val != 'nan' and user_val == correct_val:
            score += 1
    return score

# Calculate scores for all rows
if not df_responses.empty and not df_key.empty:
    df_responses['Total Score'] = df_responses.apply(lambda r: calculate_player_score(r, df_key), axis=1)
    
    # 4. Display Leaderboard
    leaderboard = df_responses[['Name', 'Total Score']].sort_values(by="Total Score", ascending=False)
    
    st.subheader("Current Standings")
    st.table(leaderboard) # or st.dataframe(leaderboard)
    
    # Optional: Add a bar chart
    st.bar_chart(data=leaderboard, x="Name", y="Total Score")
else:
    st.write("Waiting for data...")
