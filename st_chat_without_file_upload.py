from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.document_loaders import JSONLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st
import os
import json_loader_helper as jlh
import talent_passport_formatter as tpf
import json
import sys

load_dotenv()
uuid = sys.argv[1]
st.info("This is Talent's UUID: " + uuid)


def load_document():
    loader = JSONLoader(file_path=file_path, jq_schema=".", text_content=False)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000,
        chunk_overlap=20
    )
    splitDocs = splitter.split_documents(docs)
    print(len(splitDocs))
    return splitDocs


def create_db(docs):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(docs, embedding=embeddings)
    return vector_store


def get_file_path(raw_json):
    talent_uuid = raw_json['talent']['uuid']
    file_name = talent_uuid + ".json"
    folder_name = "data"
    return os.path.join(folder_name, file_name)


def creat_clean_json_file(file_path, raw_json):
    if not os.path.exists(file_path):
        # If the file doesn't exist, create it
        with open(file_path, "w") as file:
            json_dict = tpf.get_talent_passport_json_data(raw_json)
            json.dump(json_dict, file)


# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")

model = ChatOpenAI()

if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

# Get an OpenAI API Key before continuing
# Set up the LangChain, passing in Message History
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Answer the user questions based on a context: {context}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

chain = create_stuff_documents_chain(
        llm=model,
        prompt=prompt
)

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,
    input_messages_key="input",
    history_messages_key="history",
)

raw_json = jlh.get_json_from_file("tp.json")
file_path = get_file_path(raw_json)
creat_clean_json_file(file_path, raw_json)

for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    doc = load_document()
    vectorStore = create_db(doc)
    retriever = vectorStore.as_retriever(search_kwargs={"k": 2})
    retrieval_chain = create_retrieval_chain(retriever, chain_with_history)
    # Note: new messages are saved to history automatically by Langchain during run
    config = {"configurable": {"session_id": "any"}}
    response = retrieval_chain.invoke({"input": prompt}, config)
    st.chat_message("ai").write(response['answer'])

