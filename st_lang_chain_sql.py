import streamlit as st
import lang_chain_sql_helper as lch

st.title("Smart Query AI Assitant")

question = st.sidebar.text_area("What is your Database Query Question?", key="question_input")
show_query = st.sidebar.checkbox("Do you want to show SQL query?", key="show_query_checkbox")
deploy_button = st.sidebar.button("Run")

if deploy_button:
    if len(question) > 0:
        result, query, error = lch.exec(question, show_query)
      
        if len(error) < 1:
            st.header("Result:")
            st.write(result)

            if show_query and len(query) > 0:
                st.divider()
                st.header("SQL Query:")
                st.write(query)
        else:
            st.warning(error)
    else:
        st.warning("Please enter a valid question before running.")
