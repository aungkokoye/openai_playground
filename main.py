from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
  api_key=openai_api_key,
)

while True:
    question = input("What is your question? ( Type 'exit' to close the program: )\n")
    if question.lower() == 'exit':
        print("Closing the program...")
        break
    # completion = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #       {"role": "system", "content": "You are a helpful assistant."},
    #       {"role": "user", "content": question}
    #     ]
    # )
     
    print('Result!')
