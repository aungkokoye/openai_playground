import streamlit as st
import json_loader_helper as jlh
import pydantic_parser as pp

st.title("Smart Json Analysis Assitant fot Talent Passport")
question = st.sidebar.text_area("What is your Question?", key="question_input")
show_json_data = st.sidebar.checkbox("Do you want to show Json data?", key="show_json_checkbox")
deploy_button = st.sidebar.button("Run")

if deploy_button:
    if len(question) > 0:
        json_data = jlh.get_json_from_file("tp.json")
        result, talent, work_history, other_hitory, error = pp.exec(question, json_data)
     
        if len(error) < 1:
            st.header("Result:")
            st.write(result)
            
            if show_json_data:
                st.divider()
                if len(talent):
                    st.header("Talent Data:")
                    st.json(talent)
                    st.divider()
                if len(work_history):
                    st.header("Work History Data:")
                    st.json(work_history)
                    st.divider()
                if len(other_hitory):
                    st.header("Other History Data:")
                    st.json(other_hitory)
                    st.divider()          
        else:
            st.warning(error)
    else:
        st.warning("Please enter a valid question before running.")