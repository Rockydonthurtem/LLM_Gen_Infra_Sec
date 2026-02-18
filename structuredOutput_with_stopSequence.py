import os

from dotenv import load_dotenv
# from openai import OpenAI
import openai


# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Option 2 (Recommended): Use environment variable
# import os
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

model = "gpt-4o-mini"

prompt = (
    "List 1–5 key Terraform commands that begin with 'terraform' "
    "and stop after the first blank line."
)

stop_sequences = ["\n\n", "END"]

def analyze_stop(output, stop_sequences):
    detected = []
    for seq in stop_sequences:
        pos = output.find(seq)
        if pos != -1:
            detected.append((seq, pos))
    return detected


response = openai.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
    max_tokens=100,
    stop=stop_sequences
)

output = response.choices[0].message.content
finish_reason = response.choices[0].finish_reason

print("=" * 60)
print("MODEL OUTPUT:")
print(output)
print("=" * 60)

print(f"Finish reason: {finish_reason}")

stop_hits = analyze_stop(output, stop_sequences)

if stop_hits:
    for seq, pos in stop_hits:
        print(f"\nStop sequence triggered: {repr(seq)}")
        print(f"Stopped at character index: {pos}")
else:
    print("\nNo stop sequence found in returned text.")
    print("Likely stopped due to max_tokens or natural completion.")
