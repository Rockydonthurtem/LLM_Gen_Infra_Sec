import openai
import csv
from dotenv import load_dotenv
import os
from openai import OpenAI

# Set your OpenAI API key
load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

experiments = [
    {"temperature": 0.2, "max_tokens": 50, "stop": None},
    {"temperature": 0.5, "max_tokens": 100, "stop": None},
    {"temperature": 0.8, "max_tokens": 150, "stop": None}
]

# Prompt to test
prompt_text = "Write a short story about a Army Ranger school."

# CSV file to log results
csv_file = "chat_experiment_results.csv"

# Write CSV header
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Experiment", "Temperature", "Max Tokens", "Output"])

# Run experiments
for i, exp in enumerate(experiments, 1):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative storyteller."},
            {"role": "user", "content": prompt_text}
        ],
        temperature=exp["temperature"],
        max_tokens=exp["max_tokens"],
        stop=exp["stop"]
    )
    
    output_text = response.choices[0].message.content.strip()
    
    # Log to CSV
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([i, exp["temperature"], exp["max_tokens"], output_text])
    
    print(f"Experiment {i} done. Output preview:\n{output_text[:200]}...\n")

print(f"All experiments logged in {csv_file}")