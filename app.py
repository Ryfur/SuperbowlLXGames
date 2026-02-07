import streamlit as st
from streamlit_gsheets import GSheetsConnection
from urllib.parse import quote

st.title("🏆 Super Bowl LX Prop Leaderboard")

SHEET_URL = "https://docs.google.com/spreadsheets/d/1Jez5rn46YU1VV4E-qS204aX3AOoB8qg_M-KurRDPXVw/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # URL-encode the worksheet names to handle the spaces
    responses_sheet = quote("Form Responses 1")
    master_key_sheet = quote("Master Key")
    
    # Pass the encoded names to the worksheet parameter
    df_responses = conn.read(spreadsheet=SHEET_URL, worksheet=responses_sheet, ttl=0)
    df_key = conn.read(spreadsheet=SHEET_URL, worksheet=master_key_sheet, ttl=0)
    
    st.success("Connected!")
    
    # --- REST OF YOUR SCORING LOGIC HERE ---
    # Make sure your scoring logic uses the raw df_responses and df_key
    
except Exception as e:
    st.error(f"Error: {e}")
