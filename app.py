import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="Super Bowl LX Leaderboard", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Aggressive CSS to Force Light Mode (Overriding Google Sites Embed settings)
st.markdown(
    """
    <style>
    /* Force main app background to white and text to dark */
    .stApp, [data-testid="stAppViewContainer"], .main {
        background-color: #ffffff !important;
        color: #262730 !important;
    }

    /* Force the header/toolbar to be white */
    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background-color: #ffffff !important;
    }

    /* Force all text elements to dark grey */
    h1, h2, h3, p, span, div, .stMarkdown {
        color: #262730 !important;
    }

    /* Force the background of the chart container to white */
    [data-testid="stVegaLiteChart"] {
        background-color: #ffffff !important;
        border: 1px solid #f0f2f6;
        border-radius: 5px;
        padding: 10px;
    }

    /* Hide the settings and fullscreen buttons to keep the embed clean */
    button[title="Settings"], button[title="View fullscreen"] {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Data Loading Logic
# Replace with your actual Sheet ID
SHEET_ID = "1Jez5rn46YU1VV4E-qS204aX3AOoB8qg_M-KurRDPXVw"

def get_csv_url(sheet_id, tab_name):
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={tab_name}"

try:
    # Reading from renamed tabs 'Responses' and 'MasterKey'
    df_responses = pd.read_csv(get_csv_url(SHEET_ID, "Responses"))
    df_key = pd.read_csv(get_csv_url(SHEET_ID, "MasterKey"))

    # Identify the MASTER row for scoring
    master_row = df_key[df_key['Name'] == 'MASTER']

    if not master_row.empty:
        # Question columns typically start after Timestamp, Email, and Name
        question_cols = df_responses.columns[3:]
        
        def calculate_score(user_row):
            current_score = 0
            for col in question_cols:
                user_ans = str(user_row[col]).strip().lower()
                correct_ans = str(master_row[col].values[0]).strip().lower()
                
                # Only score if the master key has a value (not empty/nan)
                if correct_ans != 'nan' and user_ans == correct_ans:
                    current_score += 1
            return current_score

        # Apply scoring logic
        df_responses['Total Score'] = df_responses.apply(calculate_score, axis=1)
        
        # Prepare Leaderboard (Excluding the MASTER row itself)
        leaderboard = df_responses[df_responses['Name'] != 'MASTER']
        leaderboard = leaderboard[['Name', 'Total Score']].sort_values(by='Total Score', ascending=False)

        # 4. Display the Dashboard
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Leaderboard")
            # Using reset_index to provide a clean rank-like display
            st.table(leaderboard.reset_index(drop=True))
        
        with col2:
            st.subheader("Score Distribution")
            # theme=None is the key to preventing the chart from turning black in Google Sites
            st.bar_chart(
                data=leaderboard, 
                x="Name", 
                y="Total Score", 
                theme=None, 
                color="#d33612"
            )
            
    else:
        st.warning("Please ensure there is a row in your 'MasterKey' tab where the Name is 'MASTER'.")

except Exception as e:
    st.error(f"Connection Error: {e}")
    st.info("Ensure your Google Sheet is shared as 'Anyone with the link can view'.")
