from langchain_community.utilities import SQLDatabase
import env_helper

user = env_helper.get_sql_user()
host = env_helper.get_sql_host()
port = env_helper.get_sql_port()
db_name = env_helper.get_db_name()
password = env_helper.get_sql_password()

db_uri = "mysql+mysqlconnector://" + user + ":" + password + "@" + host + ":" + port + "/" + db_name
db = SQLDatabase.from_uri(db_uri)


def get_db():
    return db


def get_schema(_):
    return db.get_table_info()


def run_query(query):
    return db.run(query)
