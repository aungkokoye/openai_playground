import openai_helper as ai
import json 
from langchain.tools.json.tool import JsonSpec
from langchain_community.agent_toolkits import JsonToolkit
from langchain.agents import create_json_agent

llm = ai.get_chat_openai_llm()

file = "output.json"
with open(file, "r") as f1:
    data = json.load(f1)
    f1.close()
    
spec = JsonSpec(dict_=data, max_value_length=4000)
toolkit = JsonToolkit(spec=spec)

agent = create_json_agent(llm, toolkit=toolkit, max_iterations=1000, verbose=True)

response = agent.invoke("What is the user name whose age is over 40?")
    
print(data)
print(response)

# from langchain_community.document_loaders import JSONLoader

# loader = JSONLoader(
#     file_path='./output.json',
#     jq_schema='.sales',
#     text_content=False)

# data = loader.load()


# print(data)
