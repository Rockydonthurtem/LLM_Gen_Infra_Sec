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

prompt = "Explain Kubernetes network policies."

max_tokens_list = [30, 60, 120]
temperatures = [0.2, 0.8]

def analyze_output(text):
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    
    # Simple heuristic for detail level
    if word_count < 40:
        detail_level = "Low (brief explanation)"
    elif word_count < 80:
        detail_level = "Medium (moderate detail)"
    else:
        detail_level = "High (detailed explanation)"
    
    return word_count, char_count, detail_level


for temp in temperatures:
    print("\n" + "=" * 70)
    print(f"TEMPERATURE: {temp}")
    print("=" * 70)

    for max_tokens in max_tokens_list:
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temp,
            max_tokens=max_tokens
        )

        output = response.choices[0].message.content.strip()
        finish_reason = response.choices[0].finish_reason

        word_count, char_count, detail_level = analyze_output(output)

        print("\n" + "-" * 50)
        print(f"Max Tokens: {max_tokens}")
        print("-" * 50)
        print("Output:")
        print(output)
        print("\n--- Metrics ---")
        print(f"Word Count: {word_count}")
        print(f"Character Count: {char_count}")
        print(f"Detail Level: {detail_level}")
        print(f"Finish Reason: {finish_reason}")

        if finish_reason == "length":
            print("⚠️ Output was cut off due to max_tokens limit.")
        elif finish_reason == "stop":
            print("✅ Output completed naturally.")