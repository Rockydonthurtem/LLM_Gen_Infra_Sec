import os
from dotenv import load_dotenv
# from openai import OpenAI
import openai


# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# List of 5 prompts
prompts = [
    "Write a poem about Foundational Black Americans.",
    "Explain AI Platform Engineer to a fifth grader in 5 sentences.",
    "How do I give a 12 year Yorkie a great life.",
]

# Loop through prompts and query OpenAI API
for i, prompt in enumerate(prompts, start=1):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # modern replacement for text-davinci-003
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )

    answer = response.choices[0].message.content.strip()
    print(f"\nPrompt {i}: {prompt}")
    print("Response:", answer)