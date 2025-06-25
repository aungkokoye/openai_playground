import openai_helper
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import env_helper


def exec(json_data, question):
    try:
        llm = openai_helper.get_openai_llm()

        formatter_template = """
            You are a json formatter expert.
            Base on the json data below,
            {json_data}
            If json formate is not valid, modify the json data to correct json formate.
            If you need to escape, please escape as require.
            Return valid json only.
        """

        formatter_prompt = ChatPromptTemplate.from_template(formatter_template)
        formatter_chain = (
            formatter_prompt
            | llm
            | StrOutputParser()
        )

        data = formatter_chain.invoke({"json_data": json_data})
        print(data)

        json_analyzer_template = """
            You are a json data analysis expert.
            Base on the json data below,
            {data}
            Answer the user question with natural language.
            Question: {question}
        """

        json_analyzer_prompt = ChatPromptTemplate.from_template(json_analyzer_template)

        chain = (
            json_analyzer_prompt
            | llm
            | StrOutputParser()
        )

        result = chain.invoke({"question": question, "data": data})
        
        return result, data, ''

    except Exception as e:
        debug = env_helper.get_debug_mode()
        print(debug)
        error = "Something is wrong please run again!"

        if debug == "True":
            error = str(e)

        return '', '', error
    
    
if __name__ == "__main__":
    result, error = exec("output.json")
    print(result)
  
    if len(error) > 1:
        print(error)
