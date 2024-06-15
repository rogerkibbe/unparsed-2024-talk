import os
import textwrap

from dotenv import load_dotenv
from mistralai.client import MistralClient

load_dotenv()

api_key = os.environ.get("MISTRAL_API_KEY")
client = MistralClient(api_key=api_key)

the_question = input("Please enter your question: ")

# Fine-Tuned Model - replace model name with fine-tuned model
from mistralai.models.chat_completion import ChatMessage

chat_response = client.chat(
     model="ft:open-mistral-7b:c32c2392:20240613:ce61015d",
     messages=[ChatMessage(role='user', content=the_question)]
 )

print("Fine Tuned Output:")
print(textwrap.fill(chat_response.choices[0].message.content, width=80))

print ()
print ("Base model output:")

chat_response_base = client.chat(
    model="open-mistral-7b",
    messages=[ChatMessage(role='user', content=the_question)]
)
print(textwrap.fill(chat_response_base.choices[0].message.content, width=80))
