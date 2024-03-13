# OpenAI
Open API Python Application

Brew Installation

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

(echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/aungkoko/.bash_profile
eval "$(/opt/homebrew/bin/brew shellenv)"

brew --version
```

Python 3 installation

```
brew install python

pip --version

pip install python-dotenv

pip install openai

```

Set up a virtual environment

```
python -m venv <your_project_name>_env

source <your_project_name>_env/bin/activate

<your_project_name>_env\Scripts\activate
```

Create .env file

```
copy .env_example to .env
```

run command

```
python3 main.py
```