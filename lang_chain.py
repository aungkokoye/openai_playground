from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=openai_api_key)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class AI assistant."),
    ("user", "{input}")
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

while True:
    question = input("What is your question? ( Type 'exit' to close the LangChain: )\n")
    if question.lower() == 'exit':
        print("Closing LangChain ...")
        break

    result = chain.invoke({"input": question})
    print('\n\n ---------- Start LangChain Result! ---------- \n\n')
    print(result)
    print('\n\n ---------- End LangChain Result! ---------- \n\n')
