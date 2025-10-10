import streamlit as st

def load_custom_style():
    st.markdown("""
        <style>
            .stButton>button {
                background-color: #A5D6A7;
                color: black;
                border-radius: 8px;
                font-weight: 600;
            }
        </style>
    """, unsafe_allow_html=True)
