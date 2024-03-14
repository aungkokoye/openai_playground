import os
from dotenv import load_dotenv

load_dotenv()


def get_ope_api_key():
    return os.getenv("OPENAI_API_KEY")


def get_sql_user():
    return os.getenv("SQl_USER")


def get_sql_password():
    return os.getenv("SQL_PASS")


def get_sql_host():
    return os.getenv("SQL_HOST")


def get_sql_port():
    return os.getenv("SQL_PORT")


def get_db_name():
    return os.getenv("DB_NAME")
