import streamlit as st

def chat_bubble_user(msg):
    st.markdown(f"""
        <div class="chat-bubble-user">
            <strong>Você:</strong> {msg}
        </div>
    """, unsafe_allow_html=True)

def chat_bubble_bot(msg):
    st.markdown(f"""
        <div class="chat-bubble-bot">
            <strong>Teobaldo:</strong> {msg}
        </div>
    """, unsafe_allow_html=True)

