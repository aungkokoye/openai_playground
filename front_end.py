from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains import create_retrieval_chain
import streamlit as st
import os
from dotenv import load_dotenv


load_dotenv()


def load_document(doc):
    file_path = os.path.join(os.getcwd(), pdf.name)
    with open(file_path, "wb") as f:
        f.write(pdf.getvalue())
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=20
    )
    splitDocs = splitter.split_documents(docs)
    print(len(splitDocs))
    return splitDocs


def create_db(docs):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(docs, embedding= embeddings)
    return vector_store


# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")
view_messages = st.expander("View the message contents in session state")
# Get an OpenAI API Key before continuing
# Set up the LangChain, passing in Message History
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Answer the user questions based on a context: {context}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
model = ChatOpenAI()
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
# Added the file as context
pdf = st.file_uploader("Upload a PDF", type="pdf")
# Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)
# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    doc = load_document(pdf)
    vectorStore = create_db(doc)
    retriever = vectorStore.as_retriever(search_kwargs={"k": 2})
    retrieval_chain = create_retrieval_chain(retriever, chain_with_history)
    # Note: new messages are saved to history automatically by Langchain during run
    config = {"configurable": {"session_id": "any"}}
    response = retrieval_chain.invoke({"input": prompt}, config)
    st.chat_message("ai").write(response['answer'])
# Draw the messages at the end, so newly generated ones show up immediately
with view_messages:
    """
    Message History initialized with:
    ```python
    msgs = StreamlitChatMessageHistory(key="langchain_messages")
    ```
    Contents of `st.session_state.langchain_messages`:
    """
    view_messages.json(st.session_state.langchain_messages)
