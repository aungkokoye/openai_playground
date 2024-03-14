import env_helper
from langchain_openai import ChatOpenAI


def get_openai_llm():
    return ChatOpenAI(openai_api_key=env_helper.get_ope_api_key())