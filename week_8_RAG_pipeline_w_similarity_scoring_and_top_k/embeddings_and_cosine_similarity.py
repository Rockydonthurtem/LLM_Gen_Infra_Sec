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

# =======================
# STEP 1: LOAD DOCUMENTS
# =======================
doc_texts = []
doc_names = []

for filename in os.listdir("documents"):
    if filename.endswith(".txt"):
        with open(os.path.join("documents", filename), "r", encoding="utf-8") as f:
            doc_texts.append(f.read())
            doc_names.append(filename)

# =======================
# STEP 2: GET EMBEDDINGS
# =======================
def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return np.array(response.data[0].embedding)

doc_embeddings = [get_embedding(doc) for doc in doc_texts]

# =======================
# STEP 3: QUERY AND TOP-K RETRIEVAL
# =======================
query = input("Enter your query: ")
query_embedding = get_embedding(query)

similarities = cosine_similarity([query_embedding], doc_embeddings).flatten()
top_k_indices = similarities.argsort()[-TOP_K:][::-1]

retrieved_docs = [doc_texts[i] for i in top_k_indices]
retrieved_names = [doc_names[i] for i in top_k_indices]

# =======================
# STEP 4: GENERATE ANSWER
# =======================
context = "\n\n".join(retrieved_docs)
messages = [ {"role": "user", "content":f"Answer the following question using the context below:\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"}]

response = client.chat.completions.create(
    model="gpt-4",
    messages=messages
)
answer = response.choices[0].message.content.strip()

# =======================
# STEP 5: SAVE TO FILE
# =======================
output_file = "rag_output_embeddings.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"Query: {query}\n\n")
    f.write("Top-k Retrieved Documents:\n")
    for name, doc in zip(retrieved_names, retrieved_docs):
        f.write(f"\n--- {name} ---\n{doc}\n")
    f.write("\nGenerated Answer:\n")
    f.write(answer)

print(f"Results saved to {output_file}")