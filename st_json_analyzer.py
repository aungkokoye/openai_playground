import streamlit as st
import json_loader_helper as jlh
import json_analyzer_helper as jzh

st.title("Smart Json Analysis Assitant")
question = st.sidebar.text_area("What is your Question?", key="question_input")
show_json_data = st.sidebar.checkbox("Do you want to show Json data?", key="show_json_checkbox")
deploy_button = st.sidebar.button("Run")

if deploy_button:
    if len(question) > 0:
        json_data = jlh.get_json_from_file("output.json")
        result, json, error = jzh.exec(json_data, question)
     
        if len(error) < 1:
            st.header("Result:")
            st.write(result)
            
            if show_json_data:
                st.divider()
                if len(json):
                    st.header("Json Data:")
                    st.json(json)
                else:
                    st.header("Json Data: empty!")
                
        else:
            st.warning(error)
    else:
        st.warning("Please enter a valid question before running.")
