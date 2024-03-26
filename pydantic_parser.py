from langchain_core.pydantic_v1 import BaseModel, Field, HttpUrl, validator
from typing import List, Optional
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
import openai_helper as oh
import json_loader_helper as jlh
from langchain_core.output_parsers import PydanticOutputParser
import json
import re
import env_helper


class Project(BaseModel):
    poject_id: int = Field(description="Talent application project id")
    project_uuid: str = Field(description="Project uuid")
    name: str = Field(description="Project name")


class AvatarMetadata(BaseModel):
    source_url: HttpUrl = Field(description="Avatar photo link.")


class Application(BaseModel):
    appliction_id: int = Field(description="Application id")
    status: int = Field(description="Application status id")
    project: Project
    status_name: str = Field(description="Application status")


class Talent(BaseModel):
    talent_uuid: str = Field(description="Talent uuid")
    first_name: str = Field(description="Talent first name")
    last_name: str = Field(description="Talent last name.")
    email: str = Field(description="Talent email address.")
    avatar_metadata: AvatarMetadata
    applications: List[Application]
    personal_statement: str = Field(description="Talent Personal statement")
    
    @validator('personal_statement', allow_reuse=True)
    def strip_html_tags(cls, v):
  
        cleaned_statement = re.sub(r'<[^<]+?>', '', v)
        return cleaned_statement


class Taxonomy(BaseModel):
    taxonmy_id: int = Field(description="Taxonomy id")
    name: str = Field(description="Taxonomy name")

    
class Tag(BaseModel):
    tag_id: int = Field(description="Tag id")
    name: str = Field(description="Tag name")
    taxonomy: Optional[Taxonomy]
    

class EducationExperience(BaseModel):
    eduction_experience_id: int = Field(description="education experience id")
    name: str = Field("Eduction body name (school, colleage, university)")
    degree: str = Field("Degree level")
    field: str = Field("Eduction field")
    date_from: str = Field(description="starting date")
    date_to: Optional[str] = Field(description="end date")
    is_current: bool = Field(description="Currently working or not.")
    tags: List[Tag]


class EducationHistory(BaseModel):
    total_items: int = Field(description="Totle number of education history")
    education_experiences: List[EducationExperience]
    

class Industry(BaseModel):
    industry_id: int = Field(description="Industry id") 
    name: str = Field("Industry name")

    
class IndustryExperience(BaseModel):
    industry_experience_id: int = Field(description="Industry experience id")
    year: int = Field("Year of experience in industry")
    industry: Optional[Industry]

    
class IndustryHistory(BaseModel):
    total_items: int = Field(description="Totle number of industry history")
    industry_experiences: List[IndustryExperience]


class JobFunction(BaseModel):
    job_function_id: int = Field(description="Job function id") 
    name: str = Field("Job function name")


class JobFunctionExperience(BaseModel):
    job_function_experience_id: int = Field(description="Job function experience id")
    year: int = Field("Year of experience in job function")
    job_function: Optional[JobFunction]
            
    
class JobHistory(BaseModel):
    total_items: int = Field(description="Totle number of job function history")
    Job_function_experiences: List[JobFunctionExperience] 


class Language(BaseModel):
    language_id: int = Field(description="Language id")
    name: str = Field("Language name")


class LanguageExperience(BaseModel):
    language_experience_id: int = Field(description="Language experience id")
    proficiency: int = Field(description="Language proficiency level")
    language: Optional[Language]


class LanguageHistory(BaseModel):
    total_items: int = Field(description="Totle number of language history")
    langauge_experiences: List[LanguageExperience]
        

class OtherExperiences(BaseModel):
    education_history: EducationHistory
    industryHistory: IndustryHistory
    job_function_history: JobHistory
    langauge_history: LanguageHistory
    

class WorkExperience(BaseModel):
    work_experience_id: int = Field(description="work experince id")
    title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    date_from: str = Field(description="starting date")
    date_to: Optional[str] = Field(description="end date")
    is_current: bool = Field(description="Currently working or not.")
    tags: List[Tag]


class WorkHistory(BaseModel):
    total_items: int = Field(description="Totle number of work experince")
    work_experiences: List[WorkExperience]

 
def get_data(parser, template, model, json_data):
    prompt = PromptTemplate(
        template=template,
        input_variables=["json_data"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | model | parser
    result = chain.invoke({"json_data": json_data})
    return result


def object_to_json(object):
    object_dict = object.dict()  
    
    return json.dumps(object_dict, indent=4)


def exec(question, json_data):
    
    try:
        llm = oh.get_chat_openai_llm()  
        formatter_template = """
                    You are a json formatter expert.
                    Base on the json data below,
                    {json_data}
                    return valid format Json as instruct in format_instructions below.
                    {format_instructions}
                """
        parser = PydanticOutputParser(pydantic_object=Talent)
        talent = get_data(parser, formatter_template, llm, json_data)
        talent_json = object_to_json(talent)
        
        parser = PydanticOutputParser(pydantic_object=OtherExperiences)
        other_experience = get_data(parser, formatter_template, llm, json_data)
        other_experience_json = object_to_json(other_experience)

        parser = PydanticOutputParser(pydantic_object=WorkHistory)
        work_history = get_data(parser, formatter_template, llm, json_data)
        work_history_json = object_to_json(work_history)
        
        json_analyzer_template = """
                You are a json data analysis expert.
                Base on the multi json data below,
                {talent}
                {work_history}
                {other_experiences}
                Answer the user question with natural language.
                Question: {question}
                Instruction: pay attention on count            
            """

        json_analyzer_prompt = ChatPromptTemplate.from_template(json_analyzer_template)

        chain = (
                json_analyzer_prompt
                | llm
                | StrOutputParser()
            )
        
        result = chain.invoke({
            "question": question,
            "talent": talent_json,
            "work_history": work_history_json,
            "other_experiences": other_experience_json
            })
   
        return result, talent_json, work_history_json, other_experience_json, ''

    except Exception as e:
        debug = env_helper.get_debug_mode()
        error = "Something is wrong please run again!"

        if debug == "1":
            error = str(e)

        return '', '', '', '', error


if __name__ == "__main__":
    json_data = jlh.get_json_from_file("tp.json")
    result, talent_json, work_history_json, other_experience_json, error = exec(
        "What is this person experience of supply chain operations?",
        json_data
        )
    print(talent_json)
    print(work_history_json)
    print(other_experience_json)
    print(result)
