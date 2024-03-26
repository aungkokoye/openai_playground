import openai_helper
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
from langchain_text_splitters import TokenTextSplitter
import json_loader_helper as jlh
import talent_passport_formatter as tpf
import env_helper


def exec(question):   
    try:
        raw_json = jlh.get_json_from_file('tp.json')
        json_dict = tpf.get_talent_passport_json_data(raw_json)
        json_string = json.dumps(json_dict)
        text_splitter = TokenTextSplitter(chunk_size=4000, chunk_overlap=20)
        chunks = text_splitter.split_text(json_string)
        llm = openai_helper.get_openai_llm()

        json_analyzer_template = """
                    You are a json data analysis expert.
                    Base on the json data below, extratc revalent information as json format
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
            all_answers.append(answer)

        final_answer_template = """
                    You are a data analysis expert.
                    Base on the data below,
                    {data}
                    Answer the user question with natural language.
                    Question: {question}
                """
        final_answer_prompt = ChatPromptTemplate.from_template(final_answer_template)

        chain = (
                    final_answer_prompt
                    | llm
                    | StrOutputParser()
        )

        final_answer = chain.invoke({"question": question, "data": all_answers})       
        return final_answer, json_string, ''
    
    except Exception as e:
        debug = env_helper.get_debug_mode()
        error = "Something is wrong please run again!"

        if debug == "1":
            error = str(e)

        return '', '', error


if __name__ == "__main__":
    result, _, _ = exec("What is this person experience of supply chain operations?", 0)
    print(result)
