from langchain_core.pydantic_v1 import BaseModel, Field, HttpUrl
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
import openai_helper as oh
import json_loader_helper as jlh
from typing import List, Optional
from datetime import datetime
from langchain_core.output_parsers import StrOutputParser


class Taxonomy(BaseModel):
    taxonmy_id: int = Field(description="Taxonomy id")
    name: str = Field(description="Taxonomy name")

    
class Tag(BaseModel):
    tag_id: int = Field(description="Tag id")
    name: str = Field(description="Tag name")
    tagxonomy: Taxonomy


class WorkExperience(BaseModel):
    work_experience_id: int = Field(description="work experince id")
    title: str = Field(description="Job title")
    company: str = Field(description="Company name")

    date_from: datetime = Field(description="starting date")
    date_to: Optional[datetime] = Field(description="end date")
    is_current: bool = Field(description="Currently working or not.")
    tags: List[Tag]


class WorkHistory(BaseModel):
    total_items: int = Field(description="Totle number of work experince")
    work_experiences: List[WorkExperience]
    

class EducationExperience(BaseModel):
    eduction_experience_id: int = Field(description="education experience id")
    name: str = Field("Eduction body name (school, colleage, university)")
    degree: str = Field("Degree level")
    field: str = Field("Eduction field")
    date_from: datetime = Field(description="starting date")
    date_to: Optional[datetime] = Field(description="end date")
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
    industry: Industry
    

class IndustryHistory(BaseModel):
    total_items: int = Field(description="Totle number of industry history")
    industry_experiences: List[IndustryExperience]


class JobFunction(BaseModel):
    job_function_id: int = Field(description="Job function id") 
    name: str = Field("Job function name")


class JobFunctionExperience(BaseModel):
    job_function_experience_id: int = Field(description="Job function experience id")
    year: int = Field("Year of experience in job function")
    job_function: JobFunction
            
    
class JobFunctionHistory(BaseModel):
    total_items: int = Field(description="Totle number of job function history")
    Job_function_experiences: List[JobFunctionExperience] 


class Language(BaseModel):
    language_id: int = Field(description="Language id")
    name: str = Field("Language name")


class LanguageExperience(BaseModel):
    language_experience_id: int = Field(description="Language experience id")
    proficiency: int = Field(description="Language proficiency level")
    language: Language


class LanguageHistory(BaseModel):
    total_items: int = Field(description="Totle number of language history")
    langauge_experiences: List[LanguageExperience]


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


class TalentPassport(BaseModel):
    talent: Talent
    education_history: EducationHistory
    industryHistory: IndustryHistory
    job_function_history: JobFunctionHistory
    langauge_history: LanguageHistory
    work_history: WorkHistory


class OtherExperiences(BaseModel):
    education_history: EducationHistory
    industryHistory: IndustryHistory
    job_function_history: JobFunctionHistory
    langauge_history: LanguageHistory


def get_format_json_data(parser, template, llm, json_data):
    prompt = PromptTemplate(
        template=formatter_template,
        input_variables=["json_data"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | llm | parser
    result = chain.invoke({"json_data": json_data})
    return result

   
llm = oh.get_chat_openai_llm()
json_data = jlh.get_json_from_file("tp.json")   
formatter_template = """
            You are a json formatter expert.
            Base on the json data below,
            {json_data}
            return valid format json with escaped unescaped character as instruct in format_instructions below.
            {format_instructions}
        """
       
parser = JsonOutputParser(pydantic_object=Talent)
talent = get_format_json_data(parser, formatter_template, llm, json_data)
print(talent)

parser = JsonOutputParser(pydantic_object=WorkHistory)
work_history = get_format_json_data(parser, formatter_template, llm, json_data)

print(work_history)

parser = JsonOutputParser(pydantic_object=OtherExperiences)
other_experiences = get_format_json_data(parser, formatter_template, llm, json_data)

print(other_experiences)


def exec(question):

    json_analyzer_template = """
            You are a json data analysis expert.
            Base on the multi json data below,
            {talent}
            {work_history}
            {other_experiences}
            Answer the user question with natural language.
            Question: {question}
        """

    json_analyzer_prompt = ChatPromptTemplate.from_template(json_analyzer_template)

    chain = (
            json_analyzer_prompt
            | llm
            | StrOutputParser()
        )
    
    result = chain.invoke({
        "question": question,
        "talent": talent,
        "work_history": work_history,
        "other_experiences": other_experiences
        })
   
    return result


if __name__ == "__main__":
    result = exec("What is this person experience of supply chain operations?")
    print(result)
    