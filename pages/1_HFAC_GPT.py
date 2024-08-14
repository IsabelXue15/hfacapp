import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from pypdf import PdfReader
import csv
import os

st.title("💬 HFAC Chat Bot")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

pitch_dict = {}

def generate_response(input_text):
    model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
    response = model.invoke(input_text)
    st.info(response.content)


pitchFile =st.file_uploader("Upload a pitch (PDF)", type='pdf', accept_multiple_files=False)

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "Give me a summary of this pitch:",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        if not openai_api_key.startswith("sk-"):
            st.warning("Please enter your OpenAI API key!", icon="⚠")
        if pitchFile == None:
            st.warning("Please upload a pdf of a pitch", icon="⚠")
        if openai_api_key.startswith("sk-") and pitchFile is not None:
            reader = PdfReader(pitchFile)
            n = 0
            pitch = ""
            for page in reader.pages:
                pitch += page.extract_text()
            generate_response(text + pitch)