import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
import re
from pypdf import PdfReader
import csv
import os

st.title("🔗 HFAC App")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

pitch_dict = {}

def generate_response(input_text):
    model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
    response = model.invoke(input_text)
    st.info(response.content)

def save_response(input_text, name):
    model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
    response = model.invoke(input_text)
    pitch_dict[name] = response.content
    st.info(response.content)


pitchFile =st.file_uploader("Upload a pitch (PDF)", type='pdf', accept_multiple_files=True)
with st.form("recordpitch"):
    pitchSemester = st.text_input("Pitch semester")
    submitted = st.form_submit_button("Submit")

    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API key!", icon="⚠")
    else:
        if submitted:
            for singlePitch in pitchFile:
                reader = PdfReader(singlePitch)
                n = 0
                pitch = ""
                for page in reader.pages:
                    pitch += page.extract_text()
                save_response("Please format the text to be clear in your response. Ensure proper punctuation, spelling & structure. Give a detailed summary of: " + pitch, singlePitch.name)

            rows = []
            for item in pitch_dict.items():
                row = {}
                row['Pitch'] = item[0]
                row['Summary'] = item[1]
                rows.append(row)
            
            os.makedirs('pitchsummaries', exist_ok=True)
            file_path = os.path.join('pitchsummaries', f'{pitchSemester}.csv')
            with open(file_path, 'w', newline='') as csvfile:
                fieldnames = [
                    'Pitch', 'Summary'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            csvfile.close()

    









