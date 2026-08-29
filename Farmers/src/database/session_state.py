import streamlit as st

def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "latest_disease" not in st.session_state:
        st.session_state.latest_disease = None
    if "latest_soil" not in st.session_state:
        st.session_state.latest_soil = None

def append_message(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})
