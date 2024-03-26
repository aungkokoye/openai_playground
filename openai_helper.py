import env_helper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI


def get_chat_openai_llm():
    return ChatOpenAI(openai_api_key=env_helper.get_ope_api_key(), model="gpt-3.5-turbo", temperature=0)


def get_openai_llm():
    return OpenAI(openai_api_key=env_helper.get_ope_api_key(), temperature=0)
