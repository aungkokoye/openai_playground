import openai_helper
import env_helper
from langchain_core.prompts import ChatPromptTemplate
import mysql_helper
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import warnings
from sqlalchemy.exc import SAWarning


def exec(question, show_query):
    try:
        # ignore mysql table structure warnning
        warnings.filterwarnings('ignore', category=SAWarning)

        template = """
            You are a MySQL expert.
            Base on the table schema below,
            {schema}
            First create a syntactically correct MySQL query to run, accoring to user question below.
            Question: {question}
           
            SQL QUERY
            (Compatible with MySQL 5.6)

            Instructions: Please ensure that the generated SQL query does not use JSON functions such as JSON_CONTAINS, as MySQL 5.6 does not support them.
            Never query for all columns from a table. You must query only the columns that are needed to answer the question.
            Wrap each column name in backticks (`) to denote them as delimited identifiers.
            Pay attention to use only the column names you can see in the tables below. 
            Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
            Pay attention to use CURDATE() function to get the current date, if the question involves "today".
            Pay attention  Admin user contain string 'ROLE_ADMIN' in roles column.
        """

        prompt = ChatPromptTemplate.from_template(template)
        llm = openai_helper.get_openai_llm()

        sql_chain = (
            RunnablePassthrough.assign(schema=mysql_helper.get_schema)
            | prompt
            | llm.bind(stop="\nSQL Result:")
            | StrOutputParser()
        )

        main_template = """
            You are a nature language expert, transalte from mysql data to a nature language.
            Base on the table schema below, question, sql query, and sql response, write a nature language response:
            {schema}

            Question: {question}
            SQL QUERY: {query}
            SQL Response: {response}
        """

        main_prompt = ChatPromptTemplate.from_template(main_template)

        full_chain = (
            RunnablePassthrough.assign(query=sql_chain).assign(
                schema=mysql_helper.get_schema,
                response=lambda variables: mysql_helper.run_query(variables["query"])
            )
            | main_prompt
            | llm
            | StrOutputParser()
        )
        
        result = full_chain.invoke({"question": question})
        query_result = ''
      
        if show_query:
            query_result = sql_chain.invoke({"question": question})
         
        warnings.resetwarnings()

        return result, query_result, ''

    except Exception as e:
        debug = env_helper.get_debug_mode()
        error = "Something is wrong please run again!"

        if debug == "1":
            error = str(e)

        return '', '', error
