import mysql_helper as sqlHelper
from langchain.chains import create_sql_query_chain
import openai_helper as openAi


db = sqlHelper.get_db()
llm = openAi.get_chat_openai_llm()
chain = create_sql_query_chain(llm, db)

response = chain.invoke({"question": "How many admin users are there?"})

if __name__ == "__main__":
    print('w r here')
    print(response)
    print(db.run(response))
    print(chain.get_prompts()[0].pretty_print())
