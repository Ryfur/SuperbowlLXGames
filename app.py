import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("🏆 Super Bowl LX Prop Leaderboard")

# Define the clean URL directly
# Make sure this is the "Share" link set to "Anyone with the link can view"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Jez5rn46YU1VV4E-qS204aX3AOoB8qg_M-KurRDPXVw/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # We pass the spreadsheet argument directly here to bypass potential secrets errors
    df_responses = conn.read(spreadsheet=SHEET_URL, worksheet="Form Responses 1", ttl=0)
    df_key = conn.read(spreadsheet=SHEET_URL, worksheet="Master Key", ttl=0)
    st.success("Connected!")
except Exception as e:
    st.error(f"Error: {e}")
