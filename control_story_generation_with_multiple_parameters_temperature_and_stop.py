import os
from dotenv import load_dotenv
import openai


load_dotenv()
import re

# ===== CONFIG =====
API_KEY = "YOUR_API_KEY_HERE"  # or use os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"

PROMPT = "Write a 6-sentence mystery story; end before the word 'THE END'."

TEMPERATURES = [0.5, 1.0]
MAX_TOKENS_LIST = [100, 200]
STOP_SEQUENCE = ["THE END"]

OUTPUT_FILE = "creative_parameter_experiment_results.txt"
# ==================

openai.api_key = os.getenv("OPENAI_API_KEY")


def count_sentences(text):
    sentences = re.split(r'[.!?]+', text.strip())
    sentences = [s for s in sentences if s.strip()]
    return len(sentences)


def lexical_diversity(text):
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 0
    return len(set(words)) / len(words)


def analyze_output(output, finish_reason):
    word_count = len(output.split())
    sentence_count = count_sentences(output)
    diversity_score = lexical_diversity(output)

    structure_ok = (sentence_count == 6)
    stop_triggered = (finish_reason == "stop")

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "structure_ok": structure_ok,
        "diversity_score": round(diversity_score, 3),
        "finish_reason": finish_reason,
        "stop_triggered": stop_triggered
    }


def run_experiment():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("CREATIVE PARAMETER COMBINATION EXPERIMENT\n")
        f.write("=" * 80 + "\n")
        #f.write(f"Timestamp: {datetime.now()}\n")
        f.write(f"Model: {MODEL}\n")
        f.write(f"Stop Sequence: {STOP_SEQUENCE}\n")
        f.write("=" * 80 + "\n\n")

        for temp in TEMPERATURES:
            for max_tokens in MAX_TOKENS_LIST:

                f.write("=" * 80 + "\n")
                f.write(f"TEMPERATURE: {temp} | MAX_TOKENS: {max_tokens}\n")
                f.write("=" * 80 + "\n")

                response = openai.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "user", "content": PROMPT}],
                    temperature=temp,
                    max_tokens=max_tokens,
                    stop=STOP_SEQUENCE
                )

                output = response.choices[0].message.content.strip()
                finish_reason = response.choices[0].finish_reason

                analysis = analyze_output(output, finish_reason)

                # Write story
                f.write("\nStory Output:\n")
                f.write(output + "\n\n")

                # Write metrics
                f.write("--- Metrics ---\n")
                f.write(f"Word Count: {analysis['word_count']}\n")
                f.write(f"Sentence Count: {analysis['sentence_count']}\n")
                f.write(f"Structure (6 sentences met): {analysis['structure_ok']}\n")
                f.write(f"Lexical Diversity (Creativity Proxy): {analysis['diversity_score']}\n")
                f.write(f"Finish Reason: {analysis['finish_reason']}\n")
                f.write(f"Stop Triggered ('THE END'): {analysis['stop_triggered']}\n")

                # Interpret stopping behavior
                if analysis["finish_reason"] == "length":
                    f.write("⚠️ Stopped due to max_tokens limit (possible truncation).\n")
                elif analysis["finish_reason"] == "stop":
                    f.write("✅ Stopped due to stop sequence ('THE END').\n")
                else:
                    f.write("ℹ️ Natural completion.\n")

                f.write("\n\n")

    print(f"\nExperiment complete. Results saved to '{OUTPUT_FILE}'")


if __name__ == "__main__":
    run_experiment()
