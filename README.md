# OpenAI
Open API Python Application

Brew Installation

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

(echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/aungkoko/.bash_profile
eval "$(/opt/homebrew/bin/brew shellenv)"

brew --version

```

Create .env file

```
copy .env_example to .env

** need to re-run < pip install python-dotenv > if .env file change

```

Set up a virtual environment

```
brew install python

python -m venv <your_project_name>_env

source <your_project_name>_env/bin/activate

which python3

python3 --version

should show as : /Users/<your_username>/<your_project_name>/<your_project_name>_env/bin/python3

```

Python Module installation

```
pip --version

pip install python-dotenv

pip install openai

pip install langchain_openai

pip install langchain

pip install langchain-community

pip install streamlit

```

Deativate a virtual enviroment

```
rm -rf <your_project_name>_env


deactivate
```

run command

```
python3 main.py

streamlit run st_json_analyzer.py [ARGUMENTS]

```
