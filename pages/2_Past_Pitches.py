import pandas as pd
import streamlit as st
import os
import csv

st.title("🔎 Past Pitches")

path = 'pitchsummaries'

table_list = []
for filename in os.listdir(path):
    if filename.endswith('.csv'):
        table_list.append(filename)

if 'semester' not in st.session_state:
    st.session_state.semester = None

semester = st.selectbox("Select a semester", options = table_list)
if st.button("Submit"):
    st.session_state.semester = semester


if st.session_state.semester != None:
    pitch_dict = {}
    df = pd.read_csv(f'pitchsummaries/{st.session_state.semester}')
    dfval = df.values
    for line in dfval:
        pitch_dict[line[0]] = line[1]

    summary = st.selectbox("Select to view a summary", options = pitch_dict.keys())
    st.write(pitch_dict[summary])