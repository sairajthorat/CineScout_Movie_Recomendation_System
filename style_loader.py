import streamlit as st

def load_css(file_name):
    """Load CSS from external file"""
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def truncate_to_words(text, word_limit=65):
    """Truncate text to exactly specified number of words"""
    if text == "N/A" or not text:
        return "Plot information not available..."
    words = text.split()
    if len(words) <= word_limit:
        return text
    return ' '.join(words[:word_limit]) + "..."