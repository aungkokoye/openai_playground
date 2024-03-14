import openai_helper
from langchain_core.prompts import ChatPromptTemplate
import mysql_helper
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import warnings
from sqlalchemy.exc import SAWarning

# ignore mysql table structure warnning
warnings.filterwarnings('ignore', category=SAWarning)

template = """
Base on the table schema below, write a SQL qury that answer the user's question:
{schema}
admin user contain string 'ROLE_ADMIN' in roles column

Question: {question}
SQL QUERY
(Compatible with MySQL 5.6)

Instructions: Please ensure that the generated SQL query does not use JSON functions such as JSON_CONTAINS, as MySQL 5.6 does not support them.
"""

prompt = ChatPromptTemplate.from_template(template)
db = mysql_helper.get_db()
llm = openai_helper.get_openai_llm()

sql_chain = (
    RunnablePassthrough.assign(schema=mysql_helper.get_schema)
    | prompt
    | llm.bind(stop="\nSQL Result:")
    | StrOutputParser()
)

# str = db.run("Select * from user")
# str = sql_chain.invoke({"question": "How many admin user?"})

main_template = """
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

while True:
    question = input("What is DB query question? ( Type 'exit' to close the Langchain query: )\n")
    if len(question) == 0:
        print("Empty Question!")
        continue

    if question.lower() == 'exit':
        print("Closing LangChain ...")
        break

    print('\n\n ---------- Start LangChain Result! ---------- \n\n')
    print(full_chain.invoke({"question": question}))
    print('\n\n ---------- End LangChain Result! ---------- \n\n')
    
    print('\n\n ---------- Start LangChain Qurey! ---------- \n\n')
    print(sql_chain.invoke({"question": question}))
    print('\n\n ---------- End LangChain Qurey! ---------- \n\n')

# rest warnning ignore
warnings.resetwarnings()
