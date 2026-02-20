import os

from dotenv import load_dotenv
import openai


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

from datetime import datetime

# ====== CONFIGURATION ======
API_KEY = "YOUR_API_KEY_HERE"  # Or use os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
MAX_TOKENS = 150
TEMPERATURES = [0.2, 0.7, 1.0]
STOP_SEQUENCES = ["User:", "Assistant:"]

PROMPT = """User: What is graph neural network?
Assistant:"""

OUTPUT_FILE = "dialogue_stop_experiment_results.txt"

temperatures = [0.2, 0.7, 1.0]
stop_sequences = ["User:", "Assistant:"]
max_tokens = 150

def analyze_dialogue(output, finish_reason):
    word_count = len(output.split())

    # Check if model attempted to continue conversation
    continued_dialogue = any(marker in output for marker in stop_sequences)

    if finish_reason == "stop":
        stop_status = "Stopped by stop sequence"
    elif finish_reason == "length":
        stop_status = "Stopped by max_tokens"
    else:
        stop_status = f"Other: {finish_reason}"

    return word_count, continued_dialogue, stop_status


def run_experiment():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("DIALOGUE STOP SEQUENCE EXPERIMENT\n")
        f.write("=" * 70 + "\n")
        #f.write(f"Timestamp: {datetime.now()}\n")
        f.write(f"Model: {MODEL}\n")
        f.write(f"Max Tokens: {MAX_TOKENS}\n")
        f.write(f"Stop Sequences: {STOP_SEQUENCES}\n")
        f.write("=" * 70 + "\n\n")

        for temp in TEMPERATURES:
            f.write("=" * 70 + "\n")
            f.write(f"TEMPERATURE: {temp}\n")
            f.write("=" * 70 + "\n")

            response = openai.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": PROMPT}],
                temperature=temp,
                max_tokens=MAX_TOKENS,
                stop=STOP_SEQUENCES
            )

            output = response.choices[0].message.content.strip()
            finish_reason = response.choices[0].finish_reason

            word_count, continued_dialogue, stop_status = analyze_dialogue(
                output, finish_reason
            )

            # Write results to file
            f.write("\nAssistant Output:\n")
            f.write(output + "\n\n")

            f.write("--- Metrics ---\n")
            f.write(f"Word Count: {word_count}\n")
            f.write(f"Finish Reason: {finish_reason}\n")
            f.write(f"Stop Status: {stop_status}\n")
            f.write(f"Attempted Extra Dialogue Turn: {continued_dialogue}\n")

            if continued_dialogue:
                f.write("⚠️ Model attempted to continue dialogue.\n")
            else:
                f.write("✅ Model respected dialogue boundary.\n")

            f.write("\n\n")

    print(f"\nExperiment completed. Results saved to '{OUTPUT_FILE}'")


if __name__ == "__main__":
    run_experiment()
