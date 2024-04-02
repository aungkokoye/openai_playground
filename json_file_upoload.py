import talent_passport_formatter as tpf
import json_loader_helper as jlh
from langchain_text_splitters import TokenTextSplitter
import openai_helper
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
import json

raw_json = jlh.get_json_from_file("tp.json")
talent_uuid = raw_json['talent']['uuid']
file_name = talent_uuid + ".json"
folder_name = "data"
file_path = os.path.join(folder_name, file_name)
question = "what is user's work experience?"

if not os.path.exists(file_path):
    # If the file doesn't exist, create it
    with open(file_path, "w") as file:
        json_dict = tpf.get_talent_passport_json_data(raw_json)
        json.dump(json_dict, file)

with open(file_path, 'r') as file:
    json_dict = json.load(file)
    json_string = json.dumps(json_dict)

text_splitter = TokenTextSplitter(chunk_size=4000, chunk_overlap=20)
chunks = text_splitter.split_text(json_string)
llm = openai_helper.get_openai_llm()

json_analyzer_template = """
                    You are a data analysis expert.
                    Base on the data below, extratc revalent information as json format
                    {data}
                    Question: {question}
                """

json_analyzer_prompt = ChatPromptTemplate.from_template(json_analyzer_template)

chain = (
            json_analyzer_prompt
            | llm
            | StrOutputParser()
        )

all_answers = []

for chunk in chunks:
    answer = chain.invoke({"question": question, "data": chunk})
    print(answer)
    all_answers.append(answer)

final_answer_template = """
        You are a data analysis expert.
        Base on the answers below
        {answers}
        Answer the user question with natural language.
        Question: {question}
    """    
final_answer_prompt = ChatPromptTemplate.from_template(final_answer_template)

chain = (
        final_answer_prompt
        | llm
        | StrOutputParser()
    )    
    
final_answer = chain.invoke({"question": question, "answers": all_answers})  

print(final_answer)  
