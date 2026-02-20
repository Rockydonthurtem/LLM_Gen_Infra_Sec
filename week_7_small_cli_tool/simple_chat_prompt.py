# tool1_chat.py
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ERROR_LOG_FILE = "errors.txt"

def log_error(error_msg):
    with open(ERROR_LOG_FILE, "a") as f:
        f.write(error_msg + "\n")

def main():
    try:
        prompt = input("Enter your question for the LLM: ")
        response = client.chat.completions.create(
        model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        print("LLM Response:", response.choices[0].message.content)
    except Exception as e:
        error_msg = f"Error occurred: {str(e)}"
        print(error_msg)
        log_error(error_msg)

if __name__ == "__main__":
    main()