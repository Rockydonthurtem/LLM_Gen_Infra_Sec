from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# Sample Text
# -----------------------------
text = """
Artificial Intelligence is transforming industries worldwide. 
Machine learning is a subset of AI that allows systems to learn from data. 
Deep learning uses neural networks with many layers. 

Retrieval-Augmented Generation combines search with text generation. 
Chunking strategies improve retrieval accuracy. 
Sliding window chunking helps preserve context across boundaries.

Transformers were introduced in 2017 and changed NLP forever. 
Large Language Models can generate human-like responses.
"""

# ---------------------------------------------------
# 1️⃣ Fixed-Size Chunking
# ---------------------------------------------------
def fixed_size_chunking(text, chunk_size=20):
    words = text.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

# ---------------------------------------------------
# 2️⃣ Sentence-Based Chunking
# ---------------------------------------------------
def sentence_chunking(text, sentences_per_chunk=2):
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s]
    chunks = [".".join(sentences[i:i+sentences_per_chunk]) + "." 
              for i in range(0, len(sentences), sentences_per_chunk)]
    return chunks

# ---------------------------------------------------
# 3️⃣ Sliding Window Chunking
# ---------------------------------------------------
def sliding_window_chunking(text, chunk_size=20, overlap=5):
    words = text.split()
    step = chunk_size - overlap
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), step)]
    return chunks

# ---------------------------------------------------
# 4️⃣ Simple Semantic Chunking (Paragraph-Based)
# ---------------------------------------------------
def semantic_chunking(text):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    return paragraphs

# ---------------------------------------------------
# Helper: Print & Save Chunks
# ---------------------------------------------------
def print_and_save_chunks(title, chunks, file):
    divider = "=" * 50
    output = [f"\n{divider}\n{title}\n{divider}"]
    for i, chunk in enumerate(chunks):
        output.append(f"\nChunk {i+1}:\n{chunk}")
    text_block = "\n".join(output)
    
    print(text_block)  # Print to console
    file.write(text_block + "\n")  # Write to file

# ---------------------------------------------------
# Run All Strategies
# ---------------------------------------------------
if __name__ == "__main__":
    fixed_chunks = fixed_size_chunking(text)
    sentence_chunks = sentence_chunking(text)
    sliding_chunks = sliding_window_chunking(text)
    semantic_chunks = semantic_chunking(text)

    # Open the output file
    with open("chunks_output.txt", "w", encoding="utf-8") as f:
        print_and_save_chunks("Fixed Size Chunking", fixed_chunks, f)
        print_and_save_chunks("Sentence-Based Chunking", sentence_chunks, f)
        print_and_save_chunks("Sliding Window Chunking", sliding_chunks, f)
        print_and_save_chunks("Semantic (Paragraph) Chunking", semantic_chunks, f)

        # Optional: Send one chunk to OpenAI
        sample_prompt = f"Summarize this chunk:\n{fixed_chunks[0]}"
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": sample_prompt}]
        )
        summary = response.choices[0].message.content
        summary_text = f"\n{'='*50}\nOpenAI Summary of First Fixed Chunk\n{'='*50}\n{summary}\n"
        print(summary_text)
        f.write(summary_text)
