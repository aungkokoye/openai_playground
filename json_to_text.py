import talent_passport_formatter as tpf
import json_loader_helper as jlh
from langchain_text_splitters import TokenTextSplitter
import openai_helper
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import JSONLoader
import os
import json


def get_data_by_field(name, filepath):
    loader = JSONLoader(
        file_path=filepath,
        jq_schema='.'+name,
        text_content=False
        )

    return loader.load()


def get_text_content_from_json(json, information):
    prompt = """
                You are a content creation expert.
                Based on the data below, create content in natural language:
                instruction: inculde start and end date for work experiences, 
                industry experiences and job function experiences
                {data}
                This is about giving data information,
                {information}
            """
    prompt = ChatPromptTemplate.from_template(prompt)
    chain = (
        prompt
        | llm
        | StrOutputParser()
    )
    return chain.invoke({"data": json, 'information': information})


raw_json = jlh.get_json_from_file("tp.json")
talent_uuid = raw_json['talent']['uuid']
file_name = talent_uuid + ".txt"
folder_name = "data"
file_path = os.path.join(folder_name, file_name)

json_dict = tpf.get_talent_passport_json_data(raw_json)
json_string = json.dumps(json_dict)
text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=20)
chunks = text_splitter.split_text(json_string)
llm = openai_helper.get_openai_llm()

if not os.path.exists(file_path):
    # If the file doesn't exist, create it
    with open(file_path, "w") as file:
        pass
        
    with open(file_path, "a") as file:
        for chunk in chunks:
            print(chunk)

