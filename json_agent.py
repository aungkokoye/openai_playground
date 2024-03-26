import json_loader_helper as jlh
import openai_helper as oh
import json
from langchain_community.tools.json.tool import JsonSpec
from langchain.agents import create_json_agent
from langchain_community.agent_toolkits import JsonToolkit
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

output = jlh.get_json_form_loader('tp.json')
page_content = output[0].page_content
json_data = json.loads(page_content)
json_spec = JsonSpec(dict_=json_data, max_value_length=4000)

print(json_data)

llm = oh.get_openai_llm()

# formatter_template = """
#         You are a json expert.
#         Base on the json data below,
#         {json_data}
#         Change structure for meaningful json
#         Return valid json only.
#     """
        

# formatter_prompt = ChatPromptTemplate.from_template(formatter_template)
# formatter_chain = (
#     formatter_prompt
#     | llm
#     | StrOutputParser()
# )

# data = formatter_chain.invoke({"json_data": json_data})
# print(data)

json_toolkit = JsonToolkit(spec=json_spec)
json_agent_executor = create_json_agent(
    llm=llm, toolkit=json_toolkit, verbose=True
)

if __name__ == "__main__":
    result = json_agent_executor.invoke(
        "How many langugae talent can speak?"
    )
    print(result)
