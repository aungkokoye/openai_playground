import openai_helper
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = openai_helper.get_openai_llm()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class AI assistant."),
    ("user", "{input}")
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

while True:
    question = input("What is your question? ( Type 'exit' to close the Langchain: )\n")
    if question.lower() == 'exit':
        print("Closing LangChain ...")
        break

    result = chain.invoke({"input": question})
    print('\n\n ---------- Start LangChain Result! ---------- \n\n')
    print(result)
    print('\n\n ---------- End LangChain Result! ---------- \n\n')
