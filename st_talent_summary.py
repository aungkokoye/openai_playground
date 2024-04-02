import streamlit as st
import json_python_loader as jpl

st.title("Talent Summary")

talent_info_summary_button = st.sidebar.button("Talent Information Summary")
talent_work_experience_summary_button = st.sidebar.button("Talent Work Experiences Summary")
question = ''
if talent_info_summary_button:
    question = "make talent personal summary."

if talent_work_experience_summary_button:
    question = "What is talent work experiences summary?"
st.header("Result:")
if len(question) > 0:
    answer, json_data, error = jpl.exec(question)
    if len(error) < 1:
        st.write(answer)         
    else:
        st.warning(error)
