from openai import OpenAI
import os
from dotenv import load_dotenv
client = OpenAI(
api_key=os.getenv("OPENAI_API_KEY")
)

def ask_jarvis(user_input):
    completion = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role":"system","content":"You are a virtual assistant named Jarvis, skilled in general tasks like ALexa and Google Cloud."},
            {"role":"user","content":"What is coding"}
        ]
    )

    return(completion.choices[0].message.content)
