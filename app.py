import streamlit as st
import pandas as pd

st.set_page_config(page_title="Super Bowl LX Leaderboard", layout="wide")
st.title("🏆 Super Bowl LX Prop Leaderboard")

# The ID from your URL
SHEET_ID = "1Jez5rn46YU1VV4E-qS204aX3AOoB8qg_M-KurRDPXVw"

# Helper function to turn a Sheet ID and Tab Name into a CSV export URL
def get_csv_url(sheet_id, tab_name):
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={tab_name}"

try:
    # 1. Load Data directly with Pandas
    df_responses = pd.read_csv(get_csv_url(SHEET_ID, "Responses"))
    df_key = pd.read_csv(get_csv_url(SHEET_ID, "MasterKey"))

    # 2. Scoring Logic
    # We find the row in MasterKey that has 'MASTER' in the Name column
    # (Based on the files you uploaded earlier)
    master_row = df_key[df_key['Name'] == 'MASTER']

    if not master_row.empty:
        # Define the columns that are actual questions (skipping Timestamp, Email, Name)
        question_cols = df_responses.columns[3:]
        
        def calculate_score(user_row):
            current_score = 0
            for col in question_cols:
                user_ans = str(user_row[col]).strip().lower()
                correct_ans = str(master_row[col].values[0]).strip().lower()
                
                # Only score if the master key isn't empty (NaN)
                if correct_ans != 'nan' and user_ans == correct_ans:
                    current_score += 1
            return current_score

        # 3. Apply Scoring
        df_responses['Total Score'] = df_responses.apply(calculate_score, axis=1)
        
        # 4. Filter out the Master row from the leaderboard if it exists in Responses
        leaderboard = df_responses[df_responses['Name'] != 'MASTER']
        leaderboard = leaderboard[['Name', 'Total Score']].sort_values(by='Total Score', ascending=False)

        # 5. Display
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("Leaderboard")
            st.table(leaderboard.reset_index(drop=True))
        
        with col2:
            st.subheader("Score Distribution")
            st.bar_chart(data=leaderboard, x="Name", y="Total Score")
            
    else:
        st.warning("Please ensure there is a row in your MasterKey tab where the Name is 'MASTER'.")

except Exception as e:
    st.error(f"Connection Error: {e}")
    st.info("Ensure your Google Sheet is set to 'Anyone with the link can view'.")
