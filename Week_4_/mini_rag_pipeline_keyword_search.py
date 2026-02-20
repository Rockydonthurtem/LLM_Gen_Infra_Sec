import openai
import csv
from dotenv import load_dotenv
import os
from openai import OpenAI
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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
# Step 2: Keyword Index (TF-IDF)
# -------------------------
vectorizer = TfidfVectorizer()
doc_matrix = vectorizer.fit_transform(documents)

# -------------------------
# Step 3: Keyword Search
# -------------------------
def retrieve(query, top_k=3):
    query_vector = vectorizer.transform([query])
    
    similarities = cosine_similarity(query_vector, doc_matrix).flatten()
    
    top_indices = similarities.argsort()[-top_k:][::-1]
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
# Step 5: Query + Save Output
# -------------------------
query = "What is RAG?"

answer = generate_answer(query)

# Save to text file
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Query:\n")
    f.write(query + "\n\n")
    f.write("Answer:\n")
    f.write(answer)

print("Answer saved to output.txt")