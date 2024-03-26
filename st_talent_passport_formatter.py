import streamlit as st
import json_python_loader as jpl

st.title("Smart AI Assitant for Talent Passport")
question = st.sidebar.text_area("What is your question about talent?", key="question_input")
show_json_data = st.sidebar.checkbox("Do you want to show Json data?", key="show_json_checkbox")
deploy_button = st.sidebar.button("Run")

if deploy_button:
    if len(question) > 0:
        answer, json_data, error = jpl.exec(question)
     
        if len(error) < 1:
            st.header("Result:")
            st.write(answer)
            
            if show_json_data:
                st.divider()
                if len(json_data):
                    st.header("Json Data:")
                    st.json(json_data)
                else:
                    st.header("Json Data: empty!")
                
        else:
            st.warning(error)
    else:
        st.warning("Please enter a valid question before running.")
    