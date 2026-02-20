import openai
import csv
from dotenv import load_dotenv
import os
from openai import OpenAI
import numpy as np

# Set your OpenAI API key
load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------
# Step 1: Create Documents
# -------------------------
documents = [
    "Python is a popular programming language created by Guido van Rossum.",
    "Retrieval-Augmented Generation (RAG) combines retrieval and generation.",
    "Embeddings convert text into numerical vectors.",
    "Large Language Models can generate human-like text.",
    "Vector databases store embeddings for similarity search.",
    "Cosine similarity measures the angle between vectors.",
    "Transformers are deep learning models introduced in 2017.",
    "OpenAI develops advanced AI models."
]

# -------------------------
# Step 2: Create Embeddings
# -------------------------
def embed(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding)

doc_embeddings = [embed(doc) for doc in documents]

# -------------------------
# Step 3: Similarity Search
# -------------------------
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve(query, top_k=3):
    query_embedding = embed(query)
    
    similarities = [
        cosine_similarity(query_embedding, doc_embedding)
        for doc_embedding in doc_embeddings
    ]
    
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    return [documents[i] for i in top_indices]

# -------------------------
# Step 4: Generate Answer
# -------------------------
def generate_answer(query):
    retrieved_docs = retrieve(query)
    
    context = "\n".join(retrieved_docs)
    
    prompt = f"""
    Use the following context to answer the question.

    Context:
    {context}

    Question:
    {query}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You answer questions using provided context."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

# -------------------------
# Step 5: Query
# -------------------------
query = "What is RAG?"
answer = generate_answer(query)
with open("similarity_output.txt", "w", encoding="utf-8") as f:
    f.write("Query:\n")
    f.write(query + "\n\n")
    f.write("Answer:\n")
    f.write(answer)
print("Answer:\n", answer)
