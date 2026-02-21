import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TOP_K = 3
DOCUMENTS_FOLDER = "documents"

# =======================
# STEP 0: CHECK DOCUMENTS FOLDER
# =======================
if not os.path.exists(DOCUMENTS_FOLDER):
    os.makedirs(DOCUMENTS_FOLDER)
    # Optional: create a sample file to avoid empty folder issues
    with open(os.path.join(DOCUMENTS_FOLDER, "sample.txt"), "w", encoding="utf-8") as f:
        f.write("This is a sample document. Add your own text files here.")

# =======================
# STEP 1: LOAD DOCUMENTS
# =======================
doc_texts = []
doc_names = []

for filename in os.listdir(DOCUMENTS_FOLDER):
    if filename.endswith(".txt"):
        with open(os.path.join(DOCUMENTS_FOLDER, filename), "r", encoding="utf-8") as f:
            doc_texts.append(f.read())
            doc_names.append(filename)

if len(doc_texts) == 0:
    raise ValueError(f"No text files found in {DOCUMENTS_FOLDER}")

print(f"Loaded {len(doc_texts)} documents.")

# =======================
# STEP 2: VECTORIZE DOCUMENTS
# =======================
vectorizer = TfidfVectorizer()
doc_vectors = vectorizer.fit_transform(doc_texts)

# =======================
# STEP 3: QUERY AND TOP-K RETRIEVAL
# =======================
query = input("Enter your query: ")
query_vector = vectorizer.transform([query])

similarities = cosine_similarity(query_vector, doc_vectors).flatten()
top_k_indices = similarities.argsort()[-TOP_K:][::-1]

retrieved_docs = [doc_texts[i] for i in top_k_indices]
retrieved_names = [doc_names[i] for i in top_k_indices]

print("Top-k retrieved documents:")
for name, score in zip(retrieved_names, similarities[top_k_indices]):
    print(f"{name} (score: {score:.4f})")

# =======================
# STEP 4: GENERATE ANSWER USING GPT-4 CHAT COMPLETIONS
# =======================
context = "\n\n".join(retrieved_docs)

messages = [
    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
    {"role": "user", "content": f"Answer the following question using the context below:\n\nContext:\n{context}\n\nQuestion: {query}"}
]

response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    max_tokens=500,
    temperature=0.2
)

answer = response.choices[0].message.content.strip()

# =======================
# STEP 5: OUTPUT RESULTS TO TXT
# =======================
output_file = "rag_output_gpt4.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"Query: {query}\n\n")
    f.write("Top-k Retrieved Documents:\n")
    for name, doc in zip(retrieved_names, retrieved_docs):
        f.write(f"\n--- {name} ---\n{doc}\n")
    f.write("\nGenerated Answer:\n")
    f.write(answer)

print(f"\nResults saved to {output_file}")