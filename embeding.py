from langchain_openai import OpenAIEmbeddings
import json_loader_helper as jlh
import json
import talent_passport_formatter as tpf
from langchain_community.vectorstores import FAISS
import env_helper
from langchain_text_splitters import CharacterTextSplitter

key = env_helper.get_ope_api_key()
embeddings_model = OpenAIEmbeddings(openai_api_key=key)
raw_json = jlh.get_json_from_file('tp.json')
json_dict = tpf.get_talent_passport_json_data(raw_json)
json_string = json.dumps(json_dict)
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(json_string)


db = FAISS.fromstring(texts, embeddings_model)
retriever = db.as_retriever()
docs = retriever.get_relevant_documents("What is the person's experience of supply chain?")

print(docs)