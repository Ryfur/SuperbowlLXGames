import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="Super Bowl LX Leaderboard", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Aggressive CSS to Force Light Mode inside Google Sites
st.markdown(
    """
    <style>
    /* Force main app background to white */
    .stApp, [data-testid="stAppViewContainer"], .main {
        background-color: #ffffff !important;
        color: #262730 !important;
    }

    /* Force the chart container and the actual SVG chart to white */
    [data-testid="stVegaLiteChart"], 
    [data-testid="stVegaLiteChart"] svg,
    [data-testid="stVegaLiteChart"] > div {
        background-color: #ffffff !important;
    }

    /* Force all text elements to dark grey for visibility */
    h1, h2, h3, p, span, div, .stMarkdown {
        color: #262730 !important;
    }

    /* Hide Streamlit UI elements for a cleaner embed */
    [data-testid="stHeader"], [data-testid="stToolbar"] {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Data Loading Logic
SHEET_ID = "1Jez5rn46YU1VV4E-qS204aX3AOoB8qg_M-KurRDPXVw"

def get_csv_url(sheet_id, tab_name):
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={tab_name}"

try:
    df_responses = pd.read_csv(get_csv_url(SHEET_ID, "Responses"))
    df_key = pd.read_csv(get_csv_url(SHEET_ID, "MasterKey"))

    master_row = df_key[df_key['Name'] == 'MASTER']

    if not master_row.empty:
        # Columns start after Timestamp, Email, and Name
        question_cols = df_responses.columns[3:]
        
        def calculate_score(user_row):
            current_score = 0
            for col in question_cols:
                user_ans = str(user_row[col]).strip().lower()
                correct_ans = str(master_row[col].values[0]).strip().lower()
                if correct_ans != 'nan' and user_ans == correct_ans:
                    current_score += 1
            return current_score

        df_responses['Total Score'] = df_responses.apply(calculate_score, axis=1)
        
        leaderboard = df_responses[df_responses['Name'] != 'MASTER']
        leaderboard = leaderboard[['Name', 'Total Score']].sort_values(by='Total Score', ascending=False)

        # 4. Display
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Leaderboard")
            st.table(leaderboard.reset_index(drop=True))
        
        with col2:
            st.subheader("Score Distribution")
            # Removed theme=None to prevent the TypeError
            # Explicit color ensures bars are visible even if text is faint
            st.bar_chart(
                data=leaderboard, 
                x="Name", 
                y="Total Score",
                color="#d33612"
            )
            
    else:
        st.warning("Ensure there is a row in 'MasterKey' where the Name is 'MASTER'.")

except Exception as e:
    st.error(f"Connection Error: {e}")
