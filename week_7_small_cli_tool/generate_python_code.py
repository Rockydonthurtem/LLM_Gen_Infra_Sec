# tool3_generate_code.py
import datetime
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ERROR_LOG_FILE = "errors.txt"
OUTPUT_FILE = "generated_code.txt"

def log_error(error_msg):
    """Append error messages to errors.txt"""
    with open(ERROR_LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} - {error_msg}\n")

def save_output(output):
    """Save generated code to generated_code.txt"""
    with open(OUTPUT_FILE, "w") as f:
        f.write(output)
    print(f"Generated code saved to {OUTPUT_FILE}")

def main():
    try:
        task = input("Describe the Python code you want: ")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Write Python code for this task:\n{task}"}],
        )
        # Correct attribute access for ChatCompletionMessage object
        code_snippet = response.choices[0].message.content
        print("Generated Code:\n", code_snippet)
        save_output(code_snippet)
        
    except Exception as e:
        error_msg = f"Error occurred: {str(e)}"
        print(error_msg)
        log_error(error_msg)

if __name__ == "__main__":
    main()