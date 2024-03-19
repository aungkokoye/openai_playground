import json
from langchain_community.document_loaders import JSONLoader


def get_json_from_file(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
        f.close()
    return data


def get_json_form_loader(file_path):
    loader = JSONLoader(
        file_path=file_path,
        jq_schema='.',
        text_content=False
        )
    return loader.load()
